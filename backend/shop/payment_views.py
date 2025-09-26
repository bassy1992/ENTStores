import stripe
import requests
import json
import uuid
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem, Product
from .currency_service import convert_usd_to_ghs, get_rate_display
from .email_service import send_order_confirmation_email
import logging

logger = logging.getLogger(__name__)

# Stripe configuration
stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', 'sk_test_...')  # Set in settings

# MTN MoMo configuration (sandbox)
MOMO_BASE_URL = 'https://sandbox.momodeveloper.mtn.com'
MOMO_SUBSCRIPTION_KEY = getattr(settings, 'MOMO_SUBSCRIPTION_KEY', '')
MOMO_API_USER = getattr(settings, 'MOMO_API_USER', '')
MOMO_API_KEY = getattr(settings, 'MOMO_API_KEY', '')

# In-memory storage for MoMo transactions (use Redis/database in production)
momo_transactions = {}


@api_view(['POST'])
def create_stripe_checkout_session(request):
    """Create a Stripe Checkout session"""
    try:
        data = request.data
        items = data.get('items', [])
        success_url = data.get('success_url', 'http://localhost:8080/order-confirmation')
        cancel_url = data.get('cancel_url', 'http://localhost:8080/cart')
        
        if not items:
            return Response({'error': 'No items provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create line items for Stripe
        line_items = []
        for item in items:
            logger.info(f"Processing item for Stripe: {item.get('title')} - Image: {item.get('image', 'No image')}")
            
            # Handle image URL - Stripe requires absolute URLs
            image_url = item.get('image', '')
            original_image_url = image_url
            
            if image_url:
                # If it's a relative URL, make it absolute
                if image_url.startswith('/media/'):
                    image_url = f"http://localhost:8000{image_url}"
                elif image_url.startswith('media/'):
                    image_url = f"http://localhost:8000/{image_url}"
                
                # For localhost URLs in development, use a public placeholder
                if image_url.startswith('http://localhost') and settings.DEBUG:
                    image_url = "https://via.placeholder.com/400x400/007bff/ffffff?text=Product"
            
            logger.info(f"Image URL conversion: '{original_image_url}' -> '{image_url}'")
            
            # Only include images if we have a valid URL
            product_data = {
                'name': item['title'],
            }
            if image_url and (image_url.startswith('http://') or image_url.startswith('https://')):
                product_data['images'] = [image_url]
                logger.info(f"Added image to Stripe product: {image_url}")
            else:
                logger.warning(f"No valid image URL for product {item.get('title')}: '{image_url}'")
            
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': product_data,
                    'unit_amount': int(float(item['amount']) * 100),  # convert dollars to cents for Stripe
                },
                'quantity': item['quantity'],
            })
        
        # Create Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=success_url + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=cancel_url,
            metadata={
                'order_type': 'ennc_shop',
                'item_count': len(items)
            }
        )
        
        return Response({
            'url': checkout_session.url,
            'session_id': checkout_session.id
        })
        
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {e}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Checkout session error: {e}")
        return Response({'error': 'Failed to create checkout session'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def verify_stripe_session(request, session_id):
    """Verify Stripe checkout session and return session details"""
    try:
        logger.info(f"Verifying Stripe session: {session_id}")
        
        # Retrieve the session from Stripe
        session = stripe.checkout.Session.retrieve(session_id)
        logger.info(f"Session retrieved - Status: {session.payment_status}, Amount: {session.amount_total}")
        
        # Check if payment was successful - handle different statuses
        is_payment_successful = (
            session.payment_status == 'paid' or 
            (session.status == 'complete' and session.payment_status in ['paid', 'no_payment_required'])
        )
        
        if is_payment_successful:
            # Get line items to return order details
            line_items = stripe.checkout.Session.list_line_items(session_id)
            
            # Extract order information
            order_data = {
                'session_id': session.id,
                'payment_status': session.payment_status,
                'amount_total': session.amount_total,
                'currency': session.currency,
                'customer_email': session.customer_details.email if session.customer_details else None,
                'customer_name': session.customer_details.name if session.customer_details else None,
                'items': []
            }
            
            # Add line items
            for item in line_items.data:
                order_data['items'].append({
                    'name': item.description,
                    'quantity': item.quantity,
                    'amount': item.amount_total
                })
            
            # Note: Email notifications are sent in create_order() function to avoid duplicates
            logger.info(f"Payment verification successful for session: {session_id} - emails will be sent when order is created")
            
            return Response({
                'success': True,
                'session': order_data,
                'message': 'Payment verified successfully'
            })
        else:
            logger.warning(f"Payment not completed - Status: {session.payment_status} for session: {session_id}")
            return Response({
                'success': False,
                'session': {
                    'session_id': session.id,
                    'payment_status': session.payment_status,
                    'amount_total': session.amount_total,
                    'currency': session.currency
                },
                'message': f'Payment not completed. Status: {session.payment_status}',
                'error': f'Expected status "paid" but got "{session.payment_status}"'
            })
            
    except stripe.error.InvalidRequestError as e:
        logger.error(f"Invalid Stripe session ID {session_id}: {e}")
        return Response({
            'success': False,
            'error': 'Invalid session ID',
            'details': str(e)
        }, status=status.HTTP_404_NOT_FOUND)
    except stripe.error.StripeError as e:
        logger.error(f"Stripe verification error for session {session_id}: {e}")
        return Response({
            'success': False,
            'error': 'Failed to verify payment',
            'details': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Session verification error for session {session_id}: {e}")
        return Response({
            'success': False,
            'error': 'Failed to verify session',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def stripe_webhook(request):
    """Handle Stripe webhooks"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')
    
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return Response({'error': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError:
        return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Handle successful payment
        logger.info(f"Payment succeeded for session: {session['id']}")
        # You can create an order here or update order status
    
    return Response({'status': 'success'})


@api_view(['POST'])
def initiate_momo_payment(request):
    """Initiate MTN MoMo payment with currency conversion to GHS"""
    try:
        data = request.data
        phone = data.get('phone', '').strip()
        usd_amount = data.get('amount', 0)  # Amount in USD dollars
        
        if not phone or not usd_amount:
            return Response({'error': 'Phone number and amount are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Clean phone number (remove spaces, dashes, etc.)
        phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if not phone.startswith('+'):
            phone = '+233' + phone.lstrip('0')  # Assume Ghana number if no country code
        
        # Convert USD to GHS
        conversion_result = convert_usd_to_ghs(usd_amount)
        ghs_amount = conversion_result['ghs_amount_pesewas']  # Amount in pesewas
        
        logger.info(f"MoMo payment conversion: {conversion_result['usd_amount_display']} -> {conversion_result['ghs_amount_display']} (Rate: {conversion_result['exchange_rate']})")
        
        # Generate unique reference
        reference = str(uuid.uuid4())
        
        # For demo purposes, simulate MoMo API call
        # In production, you would make actual API calls to MTN MoMo with GHS amount
        
        # Simulate different responses based on phone number for testing
        if phone.endswith('1111'):  # Test number for success
            momo_transactions[reference] = {
                'status': 'pending',
                'phone': phone,
                'usd_amount': usd_amount,
                'ghs_amount': ghs_amount,
                'currency': 'GHS',
                'exchange_rate': conversion_result['exchange_rate'],
                'conversion_info': conversion_result,
                'created_at': str(uuid.uuid4())
            }
            
            # Simulate success after 5 seconds
            import threading
            def simulate_success():
                import time
                time.sleep(5)
                if reference in momo_transactions:
                    momo_transactions[reference]['status'] = 'success'
            
            threading.Thread(target=simulate_success).start()
            
        elif phone.endswith('2222'):  # Test number for failure
            momo_transactions[reference] = {
                'status': 'pending',
                'phone': phone,
                'usd_amount': usd_amount,
                'ghs_amount': ghs_amount,
                'currency': 'GHS',
                'exchange_rate': conversion_result['exchange_rate'],
                'conversion_info': conversion_result,
                'created_at': str(uuid.uuid4())
            }
            
            # Simulate failure after 3 seconds
            import threading
            def simulate_failure():
                import time
                time.sleep(3)
                if reference in momo_transactions:
                    momo_transactions[reference]['status'] = 'failed'
            
            threading.Thread(target=simulate_failure).start()
            
        else:  # Regular flow - pending status
            momo_transactions[reference] = {
                'status': 'pending',
                'phone': phone,
                'usd_amount': usd_amount,
                'ghs_amount': ghs_amount,
                'currency': 'GHS',
                'exchange_rate': conversion_result['exchange_rate'],
                'conversion_info': conversion_result,
                'created_at': str(uuid.uuid4())
            }
        
        return Response({
            'reference': reference,
            'status': 'pending',
            'message': f'Payment initiated for {conversion_result["ghs_amount_display"]}. Please check your phone for MoMo prompt.',
            'currency_conversion': {
                'original_amount': conversion_result['usd_amount_display'],
                'charged_amount': conversion_result['ghs_amount_display'],
                'exchange_rate': conversion_result['exchange_rate'],
                'rate_note': conversion_result['conversion_note']
            }
        })
        
    except Exception as e:
        logger.error(f"MoMo initiation error: {e}")
        return Response({'error': 'Failed to initiate MoMo payment'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def check_momo_status(request, reference):
    """Check MTN MoMo payment status"""
    try:
        if reference not in momo_transactions:
            return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)
        
        transaction = momo_transactions[reference]
        
        return Response({
            'reference': reference,
            'status': transaction['status'],
            'phone': transaction['phone'],
            'usd_amount': transaction.get('usd_amount', transaction.get('amount', 0)),
            'ghs_amount': transaction.get('ghs_amount', 0),
            'currency': transaction.get('currency', 'GHS'),
            'exchange_rate': transaction.get('exchange_rate'),
            'conversion_info': transaction.get('conversion_info', {})
        })
        
    except Exception as e:
        logger.error(f"MoMo status check error: {e}")
        return Response({'error': 'Failed to check payment status'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_order(request):
    """Create an order after successful payment"""
    try:
        data = request.data
        payment_reference = data.get('payment_reference', '')
        
        # Check if order already exists for this payment reference
        if payment_reference:
            existing_order = Order.objects.filter(payment_reference=payment_reference).first()
            if existing_order:
                logger.info(f"Order already exists for payment reference {payment_reference}: {existing_order.id}")
                return Response({
                    'order_id': existing_order.id,
                    'status': 'already_exists',
                    'message': 'Order already created for this payment',
                    'emails_sent': True  # Assume emails were sent when originally created
                })
        
        # Generate order ID
        order_id = f"ORD{uuid.uuid4().hex[:8].upper()}"
        
        # Calculate shipping cost from items if not provided
        calculated_shipping = data.get('shipping_cost', 0)
        if calculated_shipping == 0:
            # Calculate shipping from individual products
            items = data.get('items', [])
            for item_data in items:
                try:
                    product = Product.objects.get(id=item_data['product_id'])
                    item_shipping = getattr(product, 'shipping_cost', 9.99)  # Default $9.99
                    calculated_shipping += item_shipping * item_data.get('quantity', 1)
                except Product.DoesNotExist:
                    pass
        
        # Create order
        order = Order.objects.create(
            id=order_id,
            customer_email=data.get('customer_email', ''),
            customer_name=data.get('customer_name', ''),
            shipping_address=data.get('shipping_address', ''),
            shipping_city=data.get('shipping_city', ''),
            shipping_country=data.get('shipping_country', ''),
            shipping_postal_code=data.get('shipping_postal_code', ''),
            subtotal=data.get('subtotal', 0),
            shipping_cost=calculated_shipping,
            tax_amount=data.get('tax_amount', 0),
            total=data.get('total', 0),
            payment_method=data.get('payment_method', ''),
            payment_reference=data.get('payment_reference', ''),
            status='processing'
        )
        
        # Validate stock before creating order items
        items = data.get('items', [])
        stock_errors = []
        
        for item_data in items:
            try:
                product = Product.objects.get(id=item_data['product_id'])
                requested_quantity = item_data.get('quantity', 1)
                variant_id = item_data.get('variant_id')
                
                # Check if product is active
                if not product.is_active:
                    stock_errors.append(f"{product.title} is no longer available")
                    continue
                
                # Check variant stock if variant is specified
                if variant_id:
                    try:
                        from .models import ProductVariant
                        variant = ProductVariant.objects.get(id=variant_id, product=product)
                        if not variant.is_available:
                            stock_errors.append(f"{product.title} (selected variant) is not available")
                        elif variant.stock_quantity < requested_quantity:
                            stock_errors.append(
                                f"{product.title} (selected variant): Only {variant.stock_quantity} in stock, "
                                f"but {requested_quantity} requested"
                            )
                    except ImportError:
                        logger.warning("ProductVariant model not available, skipping variant validation")
                    except Exception as e:
                        logger.warning(f"Variant validation error: {e}")
                        stock_errors.append(f"{product.title}: Selected variant not found")
                else:
                    # Check main product stock
                    if not product.is_in_stock:
                        stock_errors.append(f"{product.title} is out of stock")
                    elif product.stock_quantity < requested_quantity:
                        stock_errors.append(
                            f"{product.title}: Only {product.stock_quantity} in stock, "
                            f"but {requested_quantity} requested"
                        )
                        
            except Product.DoesNotExist:
                stock_errors.append(f"Product with ID {item_data.get('product_id')} not found")
        
        # If there are stock errors, return them
        if stock_errors:
            logger.warning(f"Stock validation failed for order creation: {stock_errors}")
            return Response({
                'error': 'Stock validation failed',
                'stock_errors': stock_errors,
                'message': 'Some items are out of stock or unavailable'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create order items
        order_items = []
        for item_data in items:
            try:
                product = Product.objects.get(id=item_data['product_id'])
                
                # Extract variant information
                selected_size = item_data.get('selected_size', '')
                selected_color = item_data.get('selected_color', '')
                variant_id = item_data.get('variant_id')
                
                # Try to get the product variant if provided
                product_variant = None
                if variant_id:
                    try:
                        from .models import ProductVariant
                        product_variant = ProductVariant.objects.get(id=variant_id)
                        # Use variant's size and color names if not provided
                        if not selected_size and product_variant.size:
                            selected_size = product_variant.size.display_name
                        if not selected_color and product_variant.color:
                            selected_color = product_variant.color.name
                    except ImportError:
                        logger.warning("ProductVariant model not available, creating order without variant")
                    except Exception as e:
                        logger.warning(f"Product variant {variant_id} not found for order {order_id}: {e}")
                
                # Create order item with or without variant
                try:
                    order_item = OrderItem.objects.create(
                        order=order,
                        product=product,
                        product_variant=product_variant,
                        selected_size=selected_size,
                        selected_color=selected_color,
                        quantity=item_data['quantity'],
                        unit_price=item_data['unit_price']
                    )
                except Exception as e:
                    # If product_variant field doesn't exist, create without it
                    logger.warning(f"Failed to create order item with variant, trying without: {e}")
                    order_item = OrderItem.objects.create(
                        order=order,
                        product=product,
                        selected_size=selected_size,
                        selected_color=selected_color,
                        quantity=item_data['quantity'],
                        unit_price=item_data['unit_price']
                    )
                
                # Reduce stock after successful order item creation
                requested_quantity = item_data['quantity']
                try:
                    if product_variant:
                        # Reduce variant stock
                        product_variant.stock_quantity = max(0, product_variant.stock_quantity - requested_quantity)
                        product_variant.save()
                        logger.info(f"Reduced variant stock for {product.title}: {requested_quantity} units")
                    else:
                        # Reduce main product stock
                        product.stock_quantity = max(0, product.stock_quantity - requested_quantity)
                        product.save()
                        logger.info(f"Reduced product stock for {product.title}: {requested_quantity} units")
                except Exception as e:
                    logger.warning(f"Failed to reduce stock for {product.title}: {e}")
                    # Continue with order creation even if stock reduction fails
                
                # Add to email data with variant info
                variant_info = []
                if selected_size:
                    variant_info.append(f"Size: {selected_size}")
                if selected_color:
                    variant_info.append(f"Color: {selected_color}")
                
                product_name = product.title
                if variant_info:
                    product_name += f" ({', '.join(variant_info)})"
                
                order_items.append({
                    'name': product_name,
                    'sku': getattr(product, 'sku', 'N/A'),
                    'quantity': item_data['quantity'],
                    'price': f"${item_data['unit_price']:.2f}",
                    'total': f"${item_data['quantity'] * item_data['unit_price']:.2f}",
                    'variant_info': ', '.join(variant_info) if variant_info else None
                })
            except Product.DoesNotExist:
                logger.warning(f"Product {item_data['product_id']} not found for order {order_id}")
        
        # Send email notifications
        emails_sent = False
        try:
            # Send order confirmation to customer
            if order.customer_email:
                logger.info(f"Attempting to send order confirmation email to {order.customer_email} for order {order_id}")
                success = send_order_confirmation_email(order, order_items)
                if success:
                    logger.info(f"✅ Order confirmation email sent successfully to {order.customer_email} for order {order_id}")
                    emails_sent = True
                else:
                    logger.error(f"❌ Order confirmation email failed for order {order_id}")
            else:
                logger.warning(f"No customer email provided for order {order_id}")
            
            # Admin notification is now sent automatically via post_save signal
            logger.info(f"Admin notification will be sent automatically for order {order_id}")
            
        except Exception as e:
            logger.error(f"Exception while sending email notifications for order {order_id}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            # Don't fail the order creation if email fails
        
        return Response({
            'order_id': order_id,
            'status': 'created',
            'message': 'Order created successfully',
            'email_sent': emails_sent,  # Changed key name for consistency
            'customer_email': order.customer_email,  # Add for debugging
        })
        
    except Exception as e:
        logger.error(f"Order creation error: {e}")
        return Response({'error': 'Failed to create order'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Test endpoints for development
@api_view(['GET'])
def test_payments(request):
    """Test endpoint to verify payment setup"""
    rate_info = get_rate_display()
    
    return Response({
        'stripe_configured': bool(getattr(settings, 'STRIPE_SECRET_KEY', '')),
        'momo_configured': bool(getattr(settings, 'MOMO_SUBSCRIPTION_KEY', '')),
        'currency_conversion': {
            'usd_to_ghs_rate': rate_info['rate'],
            'rate_display': rate_info['display'],
            'is_cached': rate_info['is_cached'],
            'is_fallback': rate_info['is_fallback']
        },
        'test_numbers': {
            'momo_success': '+233XXXXXXX1111',
            'momo_failure': '+233XXXXXXX2222',
            'momo_pending': '+233XXXXXXX0000'
        },
        'endpoints': {
            'stripe_checkout': '/api/payments/stripe/create-checkout-session/',
            'momo_initiate': '/api/payments/momo/initiate/',
            'momo_status': '/api/payments/momo/status/{reference}/',
            'create_order': '/api/payments/create-order/',
            'exchange_rate': '/api/payments/exchange-rate/'
        }
    })

@api_view(['GET'])
def get_exchange_rate(request):
    """Get current USD to GHS exchange rate"""
    try:
        rate_info = get_rate_display()
        sample_conversion = convert_usd_to_ghs(25.00)  # $25.00 sample
        
        return Response({
            'rate': rate_info['rate'],
            'display': rate_info['display'],
            'is_cached': rate_info['is_cached'],
            'is_fallback': rate_info['is_fallback'],
            'cache_duration_seconds': rate_info['cache_duration'],
            'sample_conversion': {
                'usd_input': '$25.00',
                'ghs_output': sample_conversion['ghs_amount_display'],
                'note': sample_conversion['conversion_note']
            }
        })
        
    except Exception as e:
        logger.error(f"Exchange rate error: {e}")
        return Response({'error': 'Failed to get exchange rate'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def debug_order_creation(request):
    """Debug endpoint to check order creation requirements"""
    try:
        from .models import Product, Order, OrderItem
        
        debug_info = {
            'models_available': {
                'Product': True,
                'Order': True,
                'OrderItem': True,
            },
            'database_tables': {},
            'sample_data': {}
        }
        
        # Check if ProductVariant is available
        try:
            from .models import ProductVariant
            debug_info['models_available']['ProductVariant'] = True
            debug_info['sample_data']['variant_count'] = ProductVariant.objects.count()
        except ImportError:
            debug_info['models_available']['ProductVariant'] = False
        except Exception as e:
            debug_info['models_available']['ProductVariant'] = f"Error: {e}"
        
        # Check basic counts
        try:
            debug_info['sample_data']['product_count'] = Product.objects.count()
            debug_info['sample_data']['order_count'] = Order.objects.count()
            debug_info['sample_data']['order_item_count'] = OrderItem.objects.count()
        except Exception as e:
            debug_info['database_error'] = str(e)
        
        # Check OrderItem fields
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("PRAGMA table_info(shop_orderitem)")
                columns = cursor.fetchall()
                debug_info['orderitem_columns'] = [col[1] for col in columns]
        except Exception as e:
            debug_info['column_check_error'] = str(e)
        
        return Response(debug_info)
        
    except Exception as e:
        logger.error(f"Debug order creation error: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)