from django.core.management.base import BaseCommand
from django.db import connection
from shop.models import Product, ProductReview

class Command(BaseCommand):
    help = 'Set up review system in production'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Setting up review system...')
        
        # Check if review tables exist
        self.stdout.write('\n1️⃣ Checking review tables...')
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name LIKE '%review%'
                    ORDER BY table_name;
                """)
                tables = cursor.fetchall()
                
            if tables:
                self.stdout.write(self.style.SUCCESS(f'   ✅ Found review tables: {[t[0] for t in tables]}'))
            else:
                self.stdout.write(self.style.ERROR('   ❌ No review tables found!'))
                self.stdout.write('   Run: python manage.py migrate')
                return
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error checking tables: {e}'))
            return
        
        # Check products
        self.stdout.write('\n2️⃣ Checking products...')
        try:
            products_count = Product.objects.count()
            self.stdout.write(f'   📦 Found {products_count} products')
            
            if products_count == 0:
                self.stdout.write(self.style.WARNING('   ⚠️ No products found'))
                return
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error checking products: {e}'))
            return
        
        # Check existing reviews
        self.stdout.write('\n3️⃣ Checking existing reviews...')
        try:
            reviews_count = ProductReview.objects.count()
            self.stdout.write(f'   📝 Found {reviews_count} existing reviews')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error checking reviews: {e}'))
            return
        
        # Add sample reviews if none exist
        if reviews_count == 0:
            self.stdout.write('\n4️⃣ Adding sample reviews...')
            try:
                products = Product.objects.all()[:2]  # First 2 products
                
                sample_reviews = [
                    {
                        'user_name': 'Sarah M.',
                        'user_email': 'sarah.m@example.com',
                        'rating': 5,
                        'title': 'Amazing quality!',
                        'comment': 'This product exceeded my expectations. The material is soft and comfortable, and the fit is perfect.',
                        'verified_purchase': True
                    },
                    {
                        'user_name': 'Mike R.',
                        'user_email': 'mike.r@example.com',
                        'rating': 4,
                        'title': 'Good value for money',
                        'comment': 'Nice product overall. The color is exactly as shown in the pictures.',
                        'verified_purchase': True
                    },
                    {
                        'user_name': 'Jennifer K.',
                        'user_email': 'jennifer.k@example.com',
                        'rating': 5,
                        'title': 'Perfect fit and style',
                        'comment': 'Love this! The design is exactly what I was looking for.',
                        'verified_purchase': True
                    }
                ]
                
                created_count = 0
                for product in products:
                    for review_data in sample_reviews:
                        # Check if review already exists
                        existing = ProductReview.objects.filter(
                            product=product,
                            user_email=review_data['user_email']
                        ).first()
                        
                        if not existing:
                            ProductReview.objects.create(
                                product=product,
                                **review_data,
                                is_approved=True
                            )
                            created_count += 1
                            self.stdout.write(f'      ✅ Created review by {review_data["user_name"]} for {product.title}')
                
                self.stdout.write(self.style.SUCCESS(f'   🎉 Created {created_count} sample reviews'))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'   ❌ Error creating reviews: {e}'))
        
        # Final verification
        self.stdout.write('\n5️⃣ Final verification...')
        try:
            total_reviews = ProductReview.objects.count()
            self.stdout.write(self.style.SUCCESS(f'   📊 Total reviews: {total_reviews}'))
            
            if total_reviews > 0:
                sample = ProductReview.objects.first()
                self.stdout.write(f'   📝 Sample review: {sample.user_name} - {sample.title} ({sample.rating}★)')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error in verification: {e}'))
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Review system setup completed!'))
        self.stdout.write('📋 Next steps:')
        self.stdout.write('   1. Check admin: /admin/shop/productreview/')
        self.stdout.write('   2. Test API: /api/shop/products/{id}/reviews/')
        self.stdout.write('   3. Test frontend review loading')