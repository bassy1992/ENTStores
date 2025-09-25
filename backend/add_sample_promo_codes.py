#!/usr/bin/env python
"""
Add sample promo codes to the database
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import PromoCode

def create_sample_promo_codes():
    """Create sample promo codes for testing"""
    
    now = timezone.now()
    
    promo_codes = [
        {
            'code': 'ENNC10',
            'description': '10% off your entire order',
            'discount_type': 'percentage',
            'discount_value': 10.00,
            'minimum_order_amount': 0.00,
            'maximum_discount_amount': 50.00,
            'usage_limit': None,  # Unlimited
            'valid_from': now,
            'valid_until': now + timedelta(days=365),  # Valid for 1 year
            'is_active': True,
        },
        {
            'code': 'WELCOME20',
            'description': '20% off for new customers',
            'discount_type': 'percentage',
            'discount_value': 20.00,
            'minimum_order_amount': 50.00,
            'maximum_discount_amount': 100.00,
            'usage_limit': 100,  # Limited to 100 uses
            'valid_from': now,
            'valid_until': now + timedelta(days=90),  # Valid for 3 months
            'is_active': True,
        },
        {
            'code': 'SAVE15',
            'description': '$15 off orders over $75',
            'discount_type': 'fixed',
            'discount_value': 15.00,
            'minimum_order_amount': 75.00,
            'maximum_discount_amount': None,
            'usage_limit': None,
            'valid_from': now,
            'valid_until': now + timedelta(days=180),  # Valid for 6 months
            'is_active': True,
        },
        {
            'code': 'FREESHIP',
            'description': 'Free shipping on any order',
            'discount_type': 'free_shipping',
            'discount_value': 0.00,
            'minimum_order_amount': 0.00,
            'maximum_discount_amount': None,
            'usage_limit': None,
            'valid_from': now,
            'valid_until': now + timedelta(days=30),  # Valid for 1 month
            'is_active': True,
        },
        {
            'code': 'SUMMER25',
            'description': '25% off summer collection',
            'discount_type': 'percentage',
            'discount_value': 25.00,
            'minimum_order_amount': 100.00,
            'maximum_discount_amount': 75.00,
            'usage_limit': 50,
            'valid_from': now,
            'valid_until': now + timedelta(days=60),  # Valid for 2 months
            'is_active': True,
        },
        {
            'code': 'EXPIRED10',
            'description': 'Expired 10% off code (for testing)',
            'discount_type': 'percentage',
            'discount_value': 10.00,
            'minimum_order_amount': 0.00,
            'maximum_discount_amount': None,
            'usage_limit': None,
            'valid_from': now - timedelta(days=30),
            'valid_until': now - timedelta(days=1),  # Expired yesterday
            'is_active': True,
        },
    ]
    
    created_count = 0
    updated_count = 0
    
    for promo_data in promo_codes:
        promo_code, created = PromoCode.objects.get_or_create(
            code=promo_data['code'],
            defaults=promo_data
        )
        
        if created:
            created_count += 1
            print(f"✅ Created promo code: {promo_code.code} - {promo_code.description}")
        else:
            # Update existing promo code
            for key, value in promo_data.items():
                if key != 'code':  # Don't update the code itself
                    setattr(promo_code, key, value)
            promo_code.save()
            updated_count += 1
            print(f"🔄 Updated promo code: {promo_code.code} - {promo_code.description}")
    
    print(f"\n📊 Summary:")
    print(f"   Created: {created_count} promo codes")
    print(f"   Updated: {updated_count} promo codes")
    print(f"   Total: {PromoCode.objects.count()} promo codes in database")
    
    # Show active promo codes
    active_codes = PromoCode.objects.filter(is_active=True)
    print(f"\n🎯 Active Promo Codes:")
    for code in active_codes:
        is_valid, message = code.is_valid()
        status = "✅ Valid" if is_valid else f"❌ {message}"
        print(f"   {code.code}: {code.get_discount_display()} - {status}")

if __name__ == "__main__":
    create_sample_promo_codes()