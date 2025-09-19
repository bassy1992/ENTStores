"""
Shipping-related views and API endpoints.
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone
from django.conf import settings
import json
import logging

from .models import Order
from .email_service import send_shipping_confirmation_email, send_status_update_email

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class ShippingWebhookView(View):
    """
    Webhook endpoint for shipping providers to update order status.
    This can be used by shipping companies to automatically update order status.
    """
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['order_id', 'status']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({
                        'error': f'Missing required field: {field}'
                    }, status=400)
            
            order_id = data['order_id']
            new_status = data['status'].lower()
            tracking_number = data.get('tracking_number')
            tracking_url = data.get('tracking_url')
            carrier = data.get('carrier', 'Standard Shipping')
            estimated_delivery = data.get('estimated_delivery')
            
            # Validate status
            valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
            if new_status not in valid_statuses:
                return JsonResponse({
                    'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
                }, status=400)
            
            # Get the order
            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                return JsonResponse({
                    'error': f'Order {order_id} not found'
                }, status=404)
            
            # Update order status
            old_status = order.status
            order.status = new_status
            order.save()
            
            # Send appropriate email notification
            if new_status == 'shipped' and old_status != 'shipped':
                success = send_shipping_confirmation_email(
                    order=order,
                    tracking_number=tracking_number,
                    tracking_url=tracking_url,
                    carrier=carrier,
                    estimated_days=3
                )
                logger.info(f"Shipping confirmation sent for order {order_id}: {success}")
            
            elif new_status in ['delivered', 'cancelled'] and old_status != new_status:
                success = send_status_update_email(
                    order=order,
                    new_status=new_status.title(),
                    tracking_number=tracking_number,
                    tracking_url=tracking_url
                )
                logger.info(f"Status update email sent for order {order_id}: {success}")
            
            return JsonResponse({
                'success': True,
                'message': f'Order {order_id} status updated from {old_status} to {new_status}',
                'order_id': order_id,
                'old_status': old_status,
                'new_status': new_status,
                'tracking_number': tracking_number
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            logger.error(f"Error processing shipping webhook: {str(e)}")
            return JsonResponse({
                'error': 'Internal server error'
            }, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def update_shipping_status(request):
    """
    Simple endpoint to update shipping status.
    POST /api/shipping/update/
    {
        "order_id": "ORD123456",
        "status": "shipped",
        "tracking_number": "TRK123456789",
        "carrier": "UPS"
    }
    """
    try:
        data = json.loads(request.body)
        
        order_id = data.get('order_id')
        status = data.get('status', '').lower()
        tracking_number = data.get('tracking_number')
        carrier = data.get('carrier', 'Standard Shipping')
        
        if not order_id or not status:
            return JsonResponse({
                'error': 'order_id and status are required'
            }, status=400)
        
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return JsonResponse({
                'error': f'Order {order_id} not found'
            }, status=404)
        
        # Update status
        order.status = status
        order.save()
        
        # Generate tracking number if not provided
        if not tracking_number and status == 'shipped':
            tracking_number = f"ENT{order_id}{timezone.now().strftime('%Y%m%d')}"
        
        return JsonResponse({
            'success': True,
            'order_id': order_id,
            'status': status,
            'tracking_number': tracking_number,
            'message': f'Order {order_id} updated to {status}'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Error updating shipping status: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)


@require_http_methods(["GET"])
def get_shipping_status(request, order_id):
    """
    Get shipping status for an order.
    GET /api/shipping/status/<order_id>/
    """
    try:
        order = Order.objects.get(id=order_id)
        
        # Generate tracking number for shipped/delivered orders
        tracking_number = None
        if order.status in ['shipped', 'delivered']:
            tracking_number = f"ENT{order_id}{order.updated_at.strftime('%Y%m%d') if order.updated_at else timezone.now().strftime('%Y%m%d')}"
        
        return JsonResponse({
            'order_id': order_id,
            'status': order.status,
            'status_display': order.get_status_display(),
            'tracking_number': tracking_number,
            'customer_email': order.customer_email,
            'customer_name': order.customer_name,
            'shipping_address': {
                'address': order.shipping_address,
                'city': order.shipping_city,
                'country': order.shipping_country,
                'postal_code': order.shipping_postal_code
            },
            'created_at': order.created_at.isoformat(),
            'updated_at': order.updated_at.isoformat() if order.updated_at else None
        })
        
    except Order.DoesNotExist:
        return JsonResponse({
            'error': f'Order {order_id} not found'
        }, status=404)
    except Exception as e:
        logger.error(f"Error getting shipping status: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)


def shipping_tracking_page(request, order_id):
    """
    Simple tracking page for customers.
    GET /shipping/track/<order_id>/
    """
    try:
        order = Order.objects.get(id=order_id)
        
        # Generate tracking number
        tracking_number = None
        if order.status in ['shipped', 'delivered']:
            tracking_number = f"ENT{order_id}{order.updated_at.strftime('%Y%m%d') if order.updated_at else timezone.now().strftime('%Y%m%d')}"
        
        context = {
            'order': order,
            'tracking_number': tracking_number,
            'status_steps': [
                {'name': 'Order Placed', 'completed': True},
                {'name': 'Processing', 'completed': order.status in ['processing', 'shipped', 'delivered']},
                {'name': 'Shipped', 'completed': order.status in ['shipped', 'delivered']},
                {'name': 'Delivered', 'completed': order.status == 'delivered'},
            ]
        }
        
        from django.shortcuts import render
        return render(request, 'shipping/tracking.html', context)
        
    except Order.DoesNotExist:
        from django.http import Http404
        raise Http404(f"Order {order_id} not found")