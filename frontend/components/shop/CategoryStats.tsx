import { categoryModels } from '../../data/products';
import { Package, Star, Truck, Shield } from 'lucide-react';

export default function CategoryStats() {
  const totalProducts = categoryModels.reduce((sum, cat) => sum + (cat.productCount || 0), 0);
  const featuredCategories = categoryModels.filter(cat => cat.featured).length;

  const stats = [
    {
      icon: Package,
      value: totalProducts.toString(),
      label: 'Products Available',
      description: 'Across all categories'
    },
    {
      icon: Star,
      value: featuredCategories.toString(),
      label: 'Featured Categories',
      description: 'Handpicked collections'
    },
    {
      icon: Truck,
      value: '2-5',
      label: 'Days Shipping',
      description: 'Fast & reliable delivery'
    },
    {
      icon: Shield,
      value: '30',
      label: 'Day Returns',
      description: 'Hassle-free policy'
    }
  ];

  return (
    <section className="bg-gray-50 py-16">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900">Why Choose ENNC</h2>
          <p className="text-gray-600 mt-3 max-w-2xl mx-auto">
            We're committed to providing premium quality apparel with exceptional service
          </p>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
          {stats.map((stat, index) => (
            <div key={index} className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 text-blue-600 rounded-2xl mb-4">
                <stat.icon className="w-8 h-8" />
              </div>
              <div className="text-3xl font-bold text-gray-900 mb-2">
                {stat.value}
              </div>
              <div className="text-lg font-semibold text-gray-700 mb-1">
                {stat.label}
              </div>
              <div className="text-sm text-gray-500">
                {stat.description}
              </div>
            </div>
          ))}
        </div>

        {/* Category Breakdown */}
        <div className="mt-16 bg-white rounded-2xl p-8 shadow-sm">
          <h3 className="text-xl font-semibold text-gray-900 mb-6 text-center">
            Our Product Categories
          </h3>
          <div className="grid grid-cols-3 sm:grid-cols-4 lg:grid-cols-9 gap-4">
            {categoryModels.map((category) => (
              <div key={category.key} className="text-center">
                <div className="w-12 h-12 mx-auto mb-2 rounded-full overflow-hidden bg-gray-100">
                  <img 
                    src={category.image} 
                    alt={category.label}
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="text-xs font-medium text-gray-700 mb-1">
                  {category.label}
                </div>
                <div className="text-xs text-gray-500">
                  {category.productCount} items
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}