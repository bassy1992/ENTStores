from django.core.management.base import BaseCommand
from django.test import Client
from django.urls import reverse
from shop.models import Product, ProductReview
import json

class Command(BaseCommand):
    help = 'Test review API endpoints'

    def handle(self, *args, **options):
        client = Client()
        
        # Get a product
        product = Product.objects.first()
        if not product:
            self.stdout.write(self.style.ERROR('No products found'))
            return
        
        self.stdout.write(f'🧪 Testing review endpoints for product: {product.title}')
        
        # Test 1: GET reviews
        self.stdout.write('\n1️⃣ Testing GET reviews...')
        try:
            url = f'/api/shop/products/{product.id}/reviews/'
            response = client.get(url)
            
            self.stdout.write(f'   URL: {url}')
            self.stdout.write(f'   Status: {response.status_code}')
            
            if response.status_code == 200:
                data = response.json()
                reviews_count = len(data.get('reviews', []))
                stats = data.get('stats', {})
                
                self.stdout.write(self.style.SUCCESS(f'   ✅ Success! Found {reviews_count} reviews'))
                self.stdout.write(f'   📊 Stats: avg={stats.get("average_rating", 0)}, total={stats.get("total_reviews", 0)}')
                
                if data.get('reviews'):
                    first_review = data['reviews'][0]
                    self.stdout.write(f'   📝 First review: {first_review.get("user_name")} - {first_review.get("title")}')
            else:
                self.stdout.write(self.style.ERROR(f'   ❌ Failed: {response.content.decode()}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error: {e}'))
        
        # Test 2: POST review
        self.stdout.write('\n2️⃣ Testing POST review...')
        try:
            url = f'/api/shop/products/{product.id}/reviews/'
            
            review_data = {
                'user_name': 'Test User API',
                'user_email': 'testapi@example.com',
                'rating': 4,
                'title': 'API Test Review',
                'comment': 'This is a test review created via the Django management command to test the API endpoints.',
                'size_purchased': 'L',
                'color_purchased': 'Red'
            }
            
            response = client.post(
                url,
                data=json.dumps(review_data),
                content_type='application/json'
            )
            
            self.stdout.write(f'   URL: {url}')
            self.stdout.write(f'   Status: {response.status_code}')
            
            if response.status_code in [200, 201]:
                data = response.json()
                self.stdout.write(self.style.SUCCESS(f'   ✅ Success! Review created'))
                self.stdout.write(f'   📝 Response: {data}')
            else:
                self.stdout.write(self.style.ERROR(f'   ❌ Failed: {response.content.decode()}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error: {e}'))
        
        # Test 3: Check database
        self.stdout.write('\n3️⃣ Checking database...')
        try:
            total_reviews = ProductReview.objects.filter(product=product).count()
            self.stdout.write(f'   📊 Total reviews in database: {total_reviews}')
            
            if total_reviews > 0:
                latest_review = ProductReview.objects.filter(product=product).order_by('-created_at').first()
                self.stdout.write(f'   📝 Latest: {latest_review.user_name} - {latest_review.title} ({latest_review.rating}★)')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Database error: {e}'))
        
        self.stdout.write('\n🏁 Test completed!')