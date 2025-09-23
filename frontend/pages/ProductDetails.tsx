import Layout from '../components/layout/Layout';
import { formatPrice } from '../data/products';
import { useParams } from 'react-router-dom';
import { useCart } from '../context/cart';
import { useState, useEffect } from 'react';
import { apiService, convertApiProduct } from '../services/api';
import PageTransition from '../components/ui/PageTransition';
import { motion } from 'framer-motion';
import { getProductImageUrl } from '../lib/media';
import { ChevronLeft, ChevronRight } from 'lucide-react';

export default function ProductDetails() {
  const { slug } = useParams();
  const { add } = useCart();
  const [product, setProduct] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedImageIndex, setSelectedImageIndex] = useState(0);
  const [selectedSize, setSelectedSize] = useState<any>(null);
  const [selectedColor, setSelectedColor] = useState<any>(null);
  const [selectedVariant, setSelectedVariant] = useState<any>(null);

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

  // Update selected variant when size or color changes
  useEffect(() => {
    if (product && selectedSize && selectedColor) {
      const variant = product.variants?.find((v: any) => 
        v.size.id === selectedSize.id && v.color.id === selectedColor.id
      );
      setSelectedVariant(variant || null);
    } else {
      setSelectedVariant(null);
    }
  }, [product, selectedSize, selectedColor]);

  // Set default selections when product loads
  useEffect(() => {
    if (product && product.available_sizes?.length > 0 && !selectedSize) {
      setSelectedSize(product.available_sizes[0]);
    }
    if (product && product.available_colors?.length > 0 && !selectedColor) {
      setSelectedColor(product.available_colors[0]);
    }
  }, [product]);

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

  // Get all images (product images + main image as fallback)
  const allImages = product.images?.length > 0 
    ? product.images 
    : product.image 
      ? [{ image: product.image, alt_text: product.title, is_primary: true, order: 0 }]
      : [];

  const currentImage = allImages[selectedImageIndex] || allImages[0];

  return (
    <Layout>
      <div className="container mx-auto px-4 py-10">
        <div className="grid gap-10 lg:grid-cols-2">
          {/* Product Images */}
          <div className="space-y-4">
            {/* Main Image */}
            <div className="relative aspect-square rounded-xl border overflow-hidden bg-gray-100">
              {currentImage ? (
                <img 
                  src={getProductImageUrl(currentImage.image)} 
                  alt={currentImage.alt_text || product.title} 
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center text-gray-400">
                  <div className="text-center">
                    <div className="text-4xl mb-2">📷</div>
                    <p>Image not available</p>
                  </div>
                </div>
              )}
              
              {/* Navigation arrows for multiple images */}
              {allImages.length > 1 && (
                <>
                  <button
                    onClick={() => setSelectedImageIndex(prev => 
                      prev > 0 ? prev - 1 : allImages.length - 1
                    )}
                    className="absolute left-2 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white rounded-full p-2 shadow-lg transition-all"
                  >
                    <ChevronLeft className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => setSelectedImageIndex(prev => 
                      prev < allImages.length - 1 ? prev + 1 : 0
                    )}
                    className="absolute right-2 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white rounded-full p-2 shadow-lg transition-all"
                  >
                    <ChevronRight className="w-5 h-5" />
                  </button>
                </>
              )}
            </div>

            {/* Image Thumbnails */}
            {allImages.length > 1 && (
              <div className="flex gap-2 overflow-x-auto">
                {allImages.map((img: any, index: number) => (
                  <button
                    key={index}
                    onClick={() => setSelectedImageIndex(index)}
                    className={`flex-shrink-0 w-20 h-20 rounded-lg border-2 overflow-hidden transition-all ${
                      selectedImageIndex === index 
                        ? 'border-blue-500 ring-2 ring-blue-200' 
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <img 
                      src={getProductImageUrl(img.image)} 
                      alt={img.alt_text || `${product.title} ${index + 1}`}
                      className="w-full h-full object-cover"
                    />
                  </button>
                ))}
              </div>
            )}
          </div>
          
          {/* Product Details */}
          <div className="flex flex-col">
            <h1 className="text-3xl font-bold text-gray-900">{product.title}</h1>
            
            {/* Price */}
            <div className="mt-2">
              {selectedVariant && selectedVariant.final_price !== product.price ? (
                <div className="flex items-center gap-2">
                  <span className="text-2xl font-semibold text-gray-900">
                    {selectedVariant.final_price_display}
                  </span>
                  <span className="text-lg text-gray-500 line-through">
                    {formatPrice(product.price)}
                  </span>
                </div>
              ) : (
                <p className="text-2xl font-semibold text-gray-900">
                  {formatPrice(product.price)}
                </p>
              )}
            </div>

            <p className="mt-4 text-gray-600 leading-relaxed">{product.description}</p>

            {/* Size Selection */}
            {product.available_sizes?.length > 0 && (
              <div className="mt-6">
                <h3 className="text-sm font-medium text-gray-900 mb-3">Size</h3>
                <div className="flex flex-wrap gap-2">
                  {product.available_sizes.map((size: any) => (
                    <button
                      key={size.id}
                      onClick={() => setSelectedSize(size)}
                      className={`px-4 py-2 border rounded-md text-sm font-medium transition-all ${
                        selectedSize?.id === size.id
                          ? 'border-blue-500 bg-blue-50 text-blue-700'
                          : 'border-gray-300 text-gray-700 hover:border-gray-400'
                      }`}
                    >
                      {size.display_name}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Color Selection */}
            {product.available_colors?.length > 0 && (
              <div className="mt-6">
                <h3 className="text-sm font-medium text-gray-900 mb-3">
                  Color {selectedColor && (
                    <span className="text-gray-500 font-normal">- {selectedColor.name}</span>
                  )}
                </h3>
                <div className="flex flex-wrap gap-3">
                  {product.available_colors.map((color: any) => (
                    <button
                      key={color.id}
                      onClick={() => setSelectedColor(color)}
                      className={`w-8 h-8 rounded-full border-2 transition-all ${
                        selectedColor?.id === color.id
                          ? 'border-gray-900 ring-2 ring-gray-300'
                          : 'border-gray-300 hover:border-gray-400'
                      }`}
                      style={{ backgroundColor: color.hex_code }}
                      title={color.name}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* Stock Status */}
            {selectedVariant && (
              <div className="mt-4">
                {selectedVariant.is_in_stock ? (
                  <p className="text-sm text-green-600">
                    ✓ In stock ({selectedVariant.stock_quantity} available)
                  </p>
                ) : (
                  <p className="text-sm text-red-600">
                    ✗ Out of stock
                  </p>
                )}
              </div>
            )}
            
            {/* Action Buttons */}
            <div className="mt-6 flex gap-3">
              <button
                onClick={() => {
                  const productToAdd = {
                    ...product,
                    selectedSize: selectedSize?.name,
                    selectedColor: selectedColor?.name,
                    variant: selectedVariant
                  };
                  console.log('Adding to cart:', productToAdd);
                  add(productToAdd, 1);
                }}
                disabled={selectedVariant && !selectedVariant.is_in_stock}
                className={`flex-1 rounded-md px-6 py-3 font-medium transition-colors ${
                  selectedVariant && !selectedVariant.is_in_stock
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : 'bg-blue-600 text-white hover:bg-blue-700'
                }`}
              >
                {selectedVariant && !selectedVariant.is_in_stock ? 'Out of Stock' : 'Add to cart'}
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
