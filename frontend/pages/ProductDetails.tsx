import Layout from '../components/layout/Layout';
import { formatPrice } from '../data/products';
import { useParams } from 'react-router-dom';
import { useCart } from '../context/cart';
import { useState, useEffect } from 'react';
import { apiService, convertApiProduct } from '../services/api';
import PageTransition from '../components/ui/PageTransition';
import { motion, AnimatePresence } from 'framer-motion';
import { getProductImageUrl } from '../lib/media';
import { 
  ChevronLeft, 
  ChevronRight, 
  Star, 
  Heart, 
  Share2, 
  Truck, 
  Shield, 
  RotateCcw, 
  Zap,
  Check,
  Info,
  ArrowLeft,
  ZoomIn
} from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Separator } from '../components/ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';

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
  const [quantity, setQuantity] = useState(1);
  const [isWishlisted, setIsWishlisted] = useState(false);
  const [showImageZoom, setShowImageZoom] = useState(false);
  const [activeTab, setActiveTab] = useState('description');

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
      
      console.log('Variant search:', {
        selectedSizeId: selectedSize.id,
        selectedColorId: selectedColor.id,
        availableVariants: product.variants?.map((v: any) => ({
          sizeId: v.size.id,
          sizeName: v.size.display_name,
          colorId: v.color.id,
          colorName: v.color.name,
          stock: v.stock_quantity
        })),
        foundVariant: variant ? {
          stock: variant.stock_quantity,
          available: variant.is_available,
          inStock: variant.is_in_stock
        } : null
      });
      
      setSelectedVariant(variant || null);
      
      // If no variant found, try to auto-select a valid color for this size
      if (!variant && selectedSize) {
        const availableColorsForSize = product.variants
          ?.filter((v: any) => v.size.id === selectedSize.id && v.is_available)
          ?.map((v: any) => v.color);
        
        if (availableColorsForSize?.length > 0 && !availableColorsForSize.some(c => c.id === selectedColor.id)) {
          console.log('Auto-selecting color for size:', availableColorsForSize[0]);
          setSelectedColor(availableColorsForSize[0]);
        }
      }
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
      <PageTransition>
        <div className="min-h-screen bg-gradient-to-b from-background to-muted/20">
          {/* Breadcrumb Navigation */}
          <div className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container mx-auto px-4 py-4">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Button variant="ghost" size="sm" className="p-0 h-auto" asChild>
                  <a href="/shop" className="flex items-center gap-1 hover:text-foreground">
                    <ArrowLeft className="w-4 h-4" />
                    Back to Shop
                  </a>
                </Button>
                <span>/</span>
                <span className="text-foreground font-medium">{product.title}</span>
              </div>
            </div>
          </div>

          <div className="container mx-auto px-4 py-8">
            <div className="grid gap-8 lg:gap-12 xl:grid-cols-2">
              {/* Product Images Section */}
              <div className="space-y-4">
                {/* Main Image */}
                <Card className="overflow-hidden border-0 shadow-lg">
                  <div className="relative aspect-square bg-gradient-to-br from-muted/50 to-muted group">
                    <AnimatePresence mode="wait">
                      {currentImage ? (
                        <motion.img
                          key={selectedImageIndex}
                          initial={{ opacity: 0, scale: 1.1 }}
                          animate={{ opacity: 1, scale: 1 }}
                          exit={{ opacity: 0, scale: 0.9 }}
                          transition={{ duration: 0.3 }}
                          src={getProductImageUrl(currentImage.image)} 
                          alt={currentImage.alt_text || product.title} 
                          className="w-full h-full object-cover cursor-zoom-in"
                          onClick={() => setShowImageZoom(true)}
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center text-muted-foreground">
                          <div className="text-center">
                            <div className="text-6xl mb-4 opacity-50">📷</div>
                            <p className="text-lg">Image not available</p>
                          </div>
                        </div>
                      )}
                    </AnimatePresence>
                    
                    {/* Zoom Indicator */}
                    {currentImage && (
                      <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
                        <div className="bg-black/50 text-white p-2 rounded-full">
                          <ZoomIn className="w-4 h-4" />
                        </div>
                      </div>
                    )}
                    
                    {/* Navigation arrows */}
                    {allImages.length > 1 && (
                      <>
                        <Button
                          variant="secondary"
                          size="icon"
                          onClick={() => setSelectedImageIndex(prev => 
                            prev > 0 ? prev - 1 : allImages.length - 1
                          )}
                          className="absolute left-4 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity shadow-lg"
                        >
                          <ChevronLeft className="w-4 h-4" />
                        </Button>
                        <Button
                          variant="secondary"
                          size="icon"
                          onClick={() => setSelectedImageIndex(prev => 
                            prev < allImages.length - 1 ? prev + 1 : 0
                          )}
                          className="absolute right-4 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity shadow-lg"
                        >
                          <ChevronRight className="w-4 h-4" />
                        </Button>
                      </>
                    )}
                  </div>
                </Card>

                {/* Image Thumbnails */}
                {allImages.length > 1 && (
                  <div className="flex gap-3 overflow-x-auto pb-2">
                    {allImages.map((img: any, index: number) => (
                      <motion.button
                        key={index}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => setSelectedImageIndex(index)}
                        className={`flex-shrink-0 w-20 h-20 rounded-lg border-2 overflow-hidden transition-all ${
                          selectedImageIndex === index 
                            ? 'border-primary ring-2 ring-primary/20' 
                            : 'border-border hover:border-primary/50'
                        }`}
                      >
                        <img 
                          src={getProductImageUrl(img.image)} 
                          alt={img.alt_text || `${product.title} ${index + 1}`}
                          className="w-full h-full object-cover"
                        />
                      </motion.button>
                    ))}
                  </div>
                )}
              </div>
              
              {/* Product Details Section */}
              <div className="space-y-6">
                {/* Header */}
                <div className="space-y-4">
                  <div className="flex items-start justify-between">
                    <div className="space-y-2">
                      <h1 className="text-3xl lg:text-4xl font-bold tracking-tight">{product.title}</h1>
                      <div className="flex items-center gap-2">
                        <div className="flex items-center">
                          {[...Array(5)].map((_, i) => (
                            <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                          ))}
                        </div>
                        <span className="text-sm text-muted-foreground">(4.8) • 127 reviews</span>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="icon"
                        onClick={() => setIsWishlisted(!isWishlisted)}
                        className={isWishlisted ? 'text-red-500 border-red-200' : ''}
                      >
                        <Heart className={`w-4 h-4 ${isWishlisted ? 'fill-current' : ''}`} />
                      </Button>
                      <Button variant="outline" size="icon">
                        <Share2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                  
                  {/* Price */}
                  <div className="space-y-1">
                    {selectedVariant && selectedVariant.final_price !== product.price ? (
                      <div className="flex items-baseline gap-3">
                        <span className="text-3xl font-bold text-foreground">
                          {selectedVariant.final_price_display}
                        </span>
                        <span className="text-xl text-muted-foreground line-through">
                          {formatPrice(product.price)}
                        </span>
                        <Badge variant="destructive" className="text-xs">
                          Save {Math.round(((product.price - selectedVariant.final_price) / product.price) * 100)}%
                        </Badge>
                      </div>
                    ) : (
                      <span className="text-3xl font-bold text-foreground">
                        {formatPrice(product.price)}
                      </span>
                    )}
                    <p className="text-sm text-muted-foreground">Tax included. Shipping calculated at checkout.</p>
                  </div>
                </div>

                <Separator />

                {/* Product Options */}
                <div className="space-y-6">
                  {/* Size Selection */}
                  {product.available_sizes?.length > 0 && (
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <h3 className="font-medium">Size</h3>
                        <Button variant="link" className="h-auto p-0 text-sm">
                          Size Guide
                        </Button>
                      </div>
                      <div className="grid grid-cols-4 gap-2">
                        {product.available_sizes.map((size: any) => (
                          <Button
                            key={size.id}
                            variant={selectedSize?.id === size.id ? "default" : "outline"}
                            onClick={() => setSelectedSize(size)}
                            className="h-12"
                          >
                            {size.display_name}
                          </Button>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Color Selection */}
                  {product.available_colors?.length > 0 && (
                    <div className="space-y-3">
                      <h3 className="font-medium">
                        Color {selectedColor && (
                          <span className="text-muted-foreground font-normal">- {selectedColor.name}</span>
                        )}
                      </h3>
                      <div className="flex flex-wrap gap-3">
                        {product.available_colors.map((color: any) => {
                          const isAvailableForSize = selectedSize ? 
                            product.variants?.some((v: any) => 
                              v.size.id === selectedSize.id && 
                              v.color.id === color.id && 
                              v.is_available
                            ) : true;
                          
                          return (
                            <motion.button
                              key={color.id}
                              whileHover={{ scale: 1.1 }}
                              whileTap={{ scale: 0.9 }}
                              onClick={() => setSelectedColor(color)}
                              disabled={!isAvailableForSize}
                              className={`w-10 h-10 rounded-full border-2 transition-all relative ${
                                selectedColor?.id === color.id
                                  ? 'border-foreground ring-2 ring-primary/20'
                                  : isAvailableForSize
                                    ? 'border-border hover:border-foreground'
                                    : 'border-border opacity-50 cursor-not-allowed'
                              }`}
                              style={{ backgroundColor: color.hex_code }}
                              title={`${color.name}${!isAvailableForSize ? ' (Not available for selected size)' : ''}`}
                            >
                              {selectedColor?.id === color.id && (
                                <Check className="w-4 h-4 text-white absolute inset-0 m-auto drop-shadow-sm" />
                              )}
                              {!isAvailableForSize && (
                                <div className="absolute inset-0 flex items-center justify-center">
                                  <div className="w-8 h-0.5 bg-red-500 rotate-45"></div>
                                </div>
                              )}
                            </motion.button>
                          );
                        })}
                      </div>
                    </div>
                  )}

                  {/* Quantity & Stock */}
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <h3 className="font-medium">Quantity</h3>
                      <div className="flex items-center gap-2">
                        {/* Show variant stock if variants exist, otherwise show product stock */}
                        {selectedVariant ? (
                          selectedVariant.is_in_stock ? (
                            <Badge variant="secondary" className="text-green-600 bg-green-50">
                              <Check className="w-3 h-3 mr-1" />
                              In Stock ({selectedVariant.stock_quantity})
                            </Badge>
                          ) : (
                            <Badge variant="destructive">
                              Out of Stock
                            </Badge>
                          )
                        ) : product.variants?.length === 0 ? (
                          // Product has no variants, show main product stock
                          product.is_in_stock ? (
                            <Badge variant="secondary" className="text-green-600 bg-green-50">
                              <Check className="w-3 h-3 mr-1" />
                              In Stock ({product.stock_quantity})
                            </Badge>
                          ) : (
                            <Badge variant="destructive">
                              Out of Stock
                            </Badge>
                          )
                        ) : null}
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-3">
                      <div className="flex items-center border rounded-lg">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => setQuantity(Math.max(1, quantity - 1))}
                          disabled={quantity <= 1}
                        >
                          -
                        </Button>
                        <span className="px-4 py-2 min-w-[3rem] text-center">{quantity}</span>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => setQuantity(quantity + 1)}
                          disabled={
                            selectedVariant 
                              ? quantity >= selectedVariant.stock_quantity
                              : product.variants?.length === 0 && quantity >= product.stock_quantity
                          }
                        >
                          +
                        </Button>
                      </div>
                      
                      {!selectedVariant && selectedSize && selectedColor && (
                        <div className="flex items-center gap-2 text-orange-600">
                          <Info className="w-4 h-4" />
                          <span className="text-sm">This combination is not available</span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                <Separator />
                
                {/* Action Buttons */}
                <div className="space-y-4">
                  <div className="grid gap-3">
                    <Button
                      size="lg"
                      onClick={() => {
                        console.log('Adding to cart with variant:', {
                          product: product.title,
                          size: selectedSize?.display_name,
                          color: selectedColor?.name,
                          variantId: selectedVariant?.id,
                          quantity
                        });
                        add(
                          product, 
                          quantity, 
                          selectedSize?.display_name, 
                          selectedColor?.name, 
                          selectedVariant?.id
                        );
                      }}
                      disabled={
                        selectedVariant 
                          ? !selectedVariant.is_in_stock
                          : product.variants?.length === 0 
                            ? !product.is_in_stock
                            : true // Disable if variants exist but none selected
                      }
                      className="h-12 text-base font-medium"
                    >
                      {(() => {
                        if (selectedVariant) {
                          return selectedVariant.is_in_stock ? `Add ${quantity} to Cart` : 'Out of Stock';
                        } else if (product.variants?.length === 0) {
                          return product.is_in_stock ? `Add ${quantity} to Cart` : 'Out of Stock';
                        } else {
                          return 'Select Options';
                        }
                      })()}
                    </Button>
                    <Button variant="outline" size="lg" className="h-12" asChild>
                      <a href="/cart">View Cart</a>
                    </Button>
                  </div>
                  
                  <Button variant="secondary" size="lg" className="w-full h-12">
                    Buy Now - Express Checkout
                  </Button>
                </div>

                {/* Trust Signals */}
                <Card className="bg-muted/50">
                  <CardContent className="p-4">
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div className="flex items-center gap-2">
                        <Truck className="w-4 h-4 text-green-600" />
                        <span>Free shipping over $75</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <RotateCcw className="w-4 h-4 text-blue-600" />
                        <span>30-day returns</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Shield className="w-4 h-4 text-purple-600" />
                        <span>Secure checkout</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Zap className="w-4 h-4 text-orange-600" />
                        <span>Fast delivery</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>

            {/* Product Information Tabs */}
            <div className="mt-16">
              <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                <TabsList className="grid w-full grid-cols-4">
                  <TabsTrigger value="description">Description</TabsTrigger>
                  <TabsTrigger value="specifications">Specifications</TabsTrigger>
                  <TabsTrigger value="reviews">Reviews (127)</TabsTrigger>
                  <TabsTrigger value="shipping">Shipping & Returns</TabsTrigger>
                </TabsList>
                
                <TabsContent value="description" className="mt-6">
                  <Card>
                    <CardHeader>
                      <CardTitle>Product Description</CardTitle>
                    </CardHeader>
                    <CardContent className="prose prose-sm max-w-none">
                      <p className="text-muted-foreground leading-relaxed">
                        {product.description}
                      </p>
                      <div className="mt-6 space-y-4">
                        <h4 className="font-semibold">Key Features:</h4>
                        <ul className="space-y-2 text-muted-foreground">
                          <li>• Premium quality materials</li>
                          <li>• Comfortable fit for all-day wear</li>
                          <li>• Durable construction</li>
                          <li>• Easy care instructions</li>
                        </ul>
                      </div>
                    </CardContent>
                  </Card>
                </TabsContent>
                
                <TabsContent value="specifications" className="mt-6">
                  <Card>
                    <CardHeader>
                      <CardTitle>Specifications</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="grid gap-4">
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div className="space-y-2">
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">Material:</span>
                              <span>100% Cotton</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">Care:</span>
                              <span>Machine wash cold</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">Origin:</span>
                              <span>Made in USA</span>
                            </div>
                          </div>
                          <div className="space-y-2">
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">Weight:</span>
                              <span>0.5 lbs</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">Fit:</span>
                              <span>Regular</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">SKU:</span>
                              <span>{product.id}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </TabsContent>
                
                <TabsContent value="reviews" className="mt-6">
                  <Card>
                    <CardHeader>
                      <CardTitle>Customer Reviews</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-6">
                        <div className="flex items-center gap-4">
                          <div className="text-4xl font-bold">4.8</div>
                          <div>
                            <div className="flex items-center">
                              {[...Array(5)].map((_, i) => (
                                <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                              ))}
                            </div>
                            <p className="text-sm text-muted-foreground">Based on 127 reviews</p>
                          </div>
                        </div>
                        
                        <div className="space-y-4">
                          {[1, 2, 3].map((review) => (
                            <div key={review} className="border-b pb-4 last:border-b-0">
                              <div className="flex items-center gap-2 mb-2">
                                <div className="flex items-center">
                                  {[...Array(5)].map((_, i) => (
                                    <Star key={i} className="w-3 h-3 fill-yellow-400 text-yellow-400" />
                                  ))}
                                </div>
                                <span className="text-sm font-medium">John D.</span>
                                <span className="text-xs text-muted-foreground">2 days ago</span>
                              </div>
                              <p className="text-sm text-muted-foreground">
                                Great quality product! Fits perfectly and the material feels premium. 
                                Highly recommend this item.
                              </p>
                            </div>
                          ))}
                        </div>
                        
                        <Button variant="outline" className="w-full">
                          View All Reviews
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                </TabsContent>
                
                <TabsContent value="shipping" className="mt-6">
                  <Card>
                    <CardHeader>
                      <CardTitle>Shipping & Returns</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-6">
                      <div>
                        <h4 className="font-semibold mb-2">Shipping Information</h4>
                        <ul className="space-y-1 text-sm text-muted-foreground">
                          <li>• Free standard shipping on orders over $75</li>
                          <li>• Express shipping available for $9.99</li>
                          <li>• Orders ship within 1-2 business days</li>
                          <li>• Delivery typically takes 3-7 business days</li>
                        </ul>
                      </div>
                      
                      <div>
                        <h4 className="font-semibold mb-2">Return Policy</h4>
                        <ul className="space-y-1 text-sm text-muted-foreground">
                          <li>• 30-day return window</li>
                          <li>• Items must be in original condition</li>
                          <li>• Free return shipping</li>
                          <li>• Refunds processed within 5-7 business days</li>
                        </ul>
                      </div>
                    </CardContent>
                  </Card>
                </TabsContent>
              </Tabs>
            </div>
          </div>
        </div>
      </PageTransition>
    </Layout>
  );
}
