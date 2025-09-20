import Layout from '../components/layout/Layout';
import { formatPrice } from '../data/products';
import { useParams } from 'react-router-dom';
import { useCart } from '../context/cart';
import { useState, useEffect } from 'react';
import { apiService, convertApiProduct } from '../services/api';
import PageTransition from '../components/ui/PageTransition';
import { motion } from 'framer-motion';
import { getProductImageUrl } from '../lib/media';

export default function ProductDetails() {
  const { slug } = useParams();
  const { add } = useCart();
  const [product, setProduct] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProduct = async () => {
      if (!slug) return;
      
      try {
        setLoading(true);
        setError(null);
        console.log('Fetching product with slug:', slug);
        
        const apiProduct = await apiService.getProduct(slug);
        const convertedProduct = convertApiProduct(apiProduct);
        
        console.log('API product:', apiProduct);
        console.log('Converted product:', convertedProduct);
        
        setProduct(convertedProduct);
      } catch (err) {
        console.error('Failed to fetch product:', err);
        setError('Product not found');
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [slug]);

  if (loading) {
    return (
      <Layout>
        <div className="container mx-auto px-4 py-16">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading product...</p>
          </div>
        </div>
      </Layout>
    );
  }

  if (error || !product) {
    return (
      <Layout>
        <div className="container mx-auto px-4 py-16">
          <h1 className="text-2xl font-bold">Product not found</h1>
          <p>Looking for slug: {slug}</p>
          <p className="mt-4">The product you're looking for doesn't exist or may have been removed.</p>
          <a href="/shop" className="mt-4 inline-block text-blue-600 hover:underline">
            ← Back to Shop
          </a>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="container mx-auto px-4 py-10">
        <div className="grid gap-10 lg:grid-cols-2">
          {/* Product Image */}
          <div className="aspect-square rounded-xl border overflow-hidden bg-gray-100 flex items-center justify-center">
            {product.image ? (
              <img 
                src={getProductImageUrl(product.image)} 
                alt={product.title} 
                className="w-full h-full object-cover"
                onLoad={() => console.log('Image loaded successfully:', product.image)}
                onError={(e) => {
                  console.log('Image failed to load:', product.image);
                  const target = e.currentTarget;
                  target.style.display = 'none';
                  // Show fallback
                  const fallback = target.nextElementSibling as HTMLElement;
                  if (fallback) fallback.style.display = 'flex';
                }}
              />
            ) : null}
            {/* Fallback when image fails */}
            <div 
              className="w-full h-full flex items-center justify-center text-gray-400 bg-gray-100" 
              style={{ display: 'none' }}
            >
              <div className="text-center">
                <div className="text-4xl mb-2">📷</div>
                <p>Image not available</p>
              </div>
            </div>
          </div>
          
          {/* Product Details */}
          <div className="flex flex-col">
            <h1 className="text-3xl font-bold text-gray-900">{product.title}</h1>
            <p className="mt-2 text-2xl font-semibold text-gray-900">{formatPrice(product.price)}</p>
            <p className="mt-4 text-gray-600 leading-relaxed">{product.description}</p>
            
            {/* Debug info */}
            <div className="mt-4 p-3 bg-gray-50 rounded text-sm text-gray-600">
              <p><strong>Image URL:</strong> {product.image}</p>
              <p><strong>Category:</strong> {product.category}</p>
              <p><strong>Slug:</strong> {product.slug}</p>
            </div>
            
            {/* Action Buttons */}
            <div className="mt-6 flex gap-3">
              <button
                onClick={() => {
                  console.log('Adding to cart:', product);
                  add(product, 1);
                }}
                className="flex-1 rounded-md bg-blue-600 text-white px-6 py-3 font-medium hover:bg-blue-700 transition-colors"
              >
                Add to cart
              </button>
              <a 
                href="/cart" 
                className="rounded-md border border-gray-300 px-6 py-3 font-medium hover:bg-gray-50 transition-colors"
              >
                View cart
              </a>
            </div>
            
            {/* Product Features */}
            <div className="mt-8 text-sm text-gray-500 space-y-1">
              <p>• Free shipping over $75</p>
              <p>• 30‑day returns</p>
              <p>• Secure checkout</p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
