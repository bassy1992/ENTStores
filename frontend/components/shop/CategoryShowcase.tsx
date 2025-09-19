import { Link } from 'react-router-dom';
import { products, categoryModels, formatPrice } from '../../data/products';
import { ArrowRight, Star } from 'lucide-react';

interface CategoryShowcaseProps {
  categoryKey: string;
  title?: string;
  subtitle?: string;
}

export default function CategoryShowcase({ 
  categoryKey, 
  title,
  subtitle 
}: CategoryShowcaseProps) {
  const category = categoryModels.find(cat => cat.key === categoryKey);
  const categoryProducts = products.filter(p => p.category === categoryKey).slice(0, 4);

  if (!category || categoryProducts.length === 0) {
    return null;
  }

  return (
    <section className="container mx-auto px-4 py-16">
      <div className="grid gap-12 lg:grid-cols-2 items-center">
        {/* Category Info */}
        <div className="space-y-6">
          <div>
            {category.featured && (
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-yellow-100 text-yellow-800 text-sm font-medium mb-4">
                <Star className="w-4 h-4 fill-current" />
                Featured Category
              </div>
            )}
            <h2 className="text-4xl font-bold text-gray-900">
              {title || category.label}
            </h2>
            <p className="text-xl text-gray-600 mt-3">
              {subtitle || category.description}
            </p>
          </div>

          <div className="space-y-4">
            <div className="flex items-center gap-4 text-sm text-gray-600">
              <span className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                {category.productCount}+ Products Available
              </span>
              <span className="flex items-center gap-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                Premium Quality
              </span>
            </div>

            <div className="flex gap-4">
              <Link
                to={`/shop?c=${encodeURIComponent(category.key)}`}
                className="inline-flex items-center gap-2 bg-gray-900 text-white px-6 py-3 rounded-lg font-medium hover:bg-gray-800 transition-colors"
              >
                Shop {category.label}
                <ArrowRight className="w-4 h-4" />
              </Link>
              <Link
                to="/shop"
                className="inline-flex items-center gap-2 border border-gray-300 text-gray-700 px-6 py-3 rounded-lg font-medium hover:border-gray-400 transition-colors"
              >
                View All Categories
              </Link>
            </div>
          </div>

          {/* Category Hero Image */}
          <div className="aspect-[4/3] rounded-2xl overflow-hidden bg-gray-100 lg:hidden">
            <img 
              src={category.image} 
              alt={category.label}
              className="w-full h-full object-cover"
            />
          </div>
        </div>

        {/* Products Grid */}
        <div className="space-y-6">
          <div className="hidden lg:block aspect-[4/3] rounded-2xl overflow-hidden bg-gray-100">
            <img 
              src={category.image} 
              alt={category.label}
              className="w-full h-full object-cover"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            {categoryProducts.map((product) => (
              <Link
                key={product.id}
                to={`/product/${product.slug}`}
                className="group bg-white rounded-xl border border-gray-200 overflow-hidden hover:shadow-lg transition-all duration-300"
              >
                <div className="aspect-square bg-gray-100 overflow-hidden">
                  <img 
                    src={product.image} 
                    alt={product.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                </div>
                <div className="p-4">
                  <h3 className="font-medium text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-2">
                    {product.title}
                  </h3>
                  <p className="text-lg font-semibold text-gray-900 mt-2">
                    {formatPrice(product.price)}
                  </p>
                  {product.tags?.includes('new') && (
                    <span className="inline-block mt-2 px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
                      New
                    </span>
                  )}
                  {product.tags?.includes('bestseller') && (
                    <span className="inline-block mt-2 px-2 py-1 text-xs font-medium bg-orange-100 text-orange-800 rounded-full">
                      Bestseller
                    </span>
                  )}
                </div>
              </Link>
            ))}
          </div>

          <div className="text-center">
            <Link
              to={`/shop?c=${encodeURIComponent(category.key)}`}
              className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 font-medium"
            >
              View all {category.label.toLowerCase()}
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}