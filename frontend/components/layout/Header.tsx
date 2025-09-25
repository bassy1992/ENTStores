import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { useCart } from '../../context/cart';
import { cn } from '../../lib/utils';
import { apiService, convertApiCategory } from '../../services/api';
import { 
  Search, 
  ShoppingBag, 
  Menu, 
  X, 
  User, 
  Heart,
  ChevronDown,
  Package,
  Headphones,
  Shirt,
  Crown
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function Header() {
  const { count } = useCart();
  const [q, setQ] = useState('');
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const [showCategories, setShowCategories] = useState(false);
  const [categories, setCategories] = useState<any[]>([]);
  const [categoriesLoading, setCategoriesLoading] = useState(true);
  const navigate = useNavigate();
  const location = useLocation();

  // Handle scroll effect
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Fetch categories from API
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        setCategoriesLoading(true);
        const response = await apiService.getCategories();
        const convertedCategories = response.map(convertApiCategory);
        setCategories(convertedCategories);
      } catch (error) {
        console.error('Failed to fetch categories:', error);
        // Fallback to hardcoded categories if API fails
        setCategories([
          { key: 't-shirts', label: 'T-Shirts', icon: Shirt },
          { key: 'hoodies', label: 'Hoodies', icon: Crown },
          { key: 'accessories', label: 'Accessories', icon: Package },
        ]);
      } finally {
        setCategoriesLoading(false);
      }
    };

    fetchCategories();
  }, []);

  // Close mobile menu on route change
  useEffect(() => {
    setIsMenuOpen(false);
    setShowCategories(false);
  }, [location]);

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    const query = q.trim();
    if (query) navigate(`/search?q=${encodeURIComponent(query)}`);
  };

  // Helper function to get icon for category
  const getCategoryIcon = (categoryKey: string) => {
    const iconMap: { [key: string]: any } = {
      't-shirts': Shirt,
      'polos': Shirt,
      'hoodies': Crown,
      'sweatshirts': Crown,
      'tracksuits': Package,
      'jackets': Package,
      'shorts': Shirt,
      'headwear': Crown,
      'accessories': Package,
    };
    return iconMap[categoryKey] || Package;
  };

  const isActiveLink = (path: string) => {
    return location.pathname === path;
  };

  return (
    <>
      <header className={cn(
        "sticky top-0 z-50 transition-all duration-300",
        isScrolled 
          ? "backdrop-blur-md bg-white/95 shadow-lg border-b border-gray-200" 
          : "bg-white border-b border-gray-100"
      )}>
        {/* Top Bar */}
        <div className="bg-gray-900 text-white py-2 px-4">
          <div className="max-w-7xl mx-auto flex justify-between items-center text-sm">
            <div className="flex items-center gap-4">
              <span>Free shipping on orders over $75</span>
              <span className="hidden md:inline">•</span>
              <span className="hidden md:inline">30-day returns</span>
            </div>
            <div className="flex items-center gap-4">
              <Link to="/contact" className="hover:text-gray-300 transition-colors">
                <Headphones className="w-4 h-4 inline mr-1" />
                Support
              </Link>
            </div>
          </div>
        </div>

        {/* Main Header */}
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            
            {/* Logo */}
            <Link to="/" className="flex items-center gap-3 group">
              <img 
                src="https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fa7419136808a40ba94992db25a691b96?format=webp&width=200" 
                alt="ENNC logo" 
                className="h-8 w-auto transition-transform group-hover:scale-105" 
              />
              <span className="font-bold text-2xl tracking-tight text-gray-900">ENNC</span>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden lg:flex items-center gap-8">
              <Link 
                to="/shop" 
                className={cn(
                  "font-medium transition-colors hover:text-blue-600 relative py-2",
                  isActiveLink('/shop') ? "text-blue-600" : "text-gray-700"
                )}
              >
                Shop
                {isActiveLink('/shop') && (
                  <motion.div 
                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600"
                    layoutId="activeTab"
                  />
                )}
              </Link>
              
              <div 
                className="relative"
                onMouseEnter={() => setShowCategories(true)}
                onMouseLeave={() => setShowCategories(false)}
              >
                <Link 
                  to="/categories" 
                  className={cn(
                    "font-medium transition-colors hover:text-blue-600 relative py-2 flex items-center gap-1",
                    isActiveLink('/categories') ? "text-blue-600" : "text-gray-700"
                  )}
                >
                  Categories
                  <ChevronDown className="w-4 h-4" />
                  {isActiveLink('/categories') && (
                    <motion.div 
                      className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600"
                      layoutId="activeTab"
                    />
                  )}
                </Link>
                
                {/* Categories Dropdown */}
                <AnimatePresence>
                  {showCategories && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: 10 }}
                      className="absolute top-full left-0 mt-2 w-64 bg-white rounded-lg shadow-xl border border-gray-200 py-2"
                    >
                      {categoriesLoading ? (
                        <div className="px-4 py-3 text-gray-500 text-sm">Loading categories...</div>
                      ) : (
                        categories.map((category) => {
                          const Icon = getCategoryIcon(category.key);
                          return (
                            <Link
                              key={category.key}
                              to={`/shop?category=${category.key}`}
                              className="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition-colors"
                            >
                              <Icon className="w-5 h-5 text-gray-400" />
                              <span className="font-medium text-gray-700">{category.label}</span>
                              {category.productCount > 0 && (
                                <span className="ml-auto text-xs text-gray-400">
                                  {category.productCount}
                                </span>
                              )}
                            </Link>
                          );
                        })
                      )}
                      <div className="border-t border-gray-100 mt-2 pt-2">
                        <Link
                          to="/categories"
                          className="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition-colors text-blue-600 font-medium"
                        >
                          View All Categories
                        </Link>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
              
              <Link 
                to="/contact" 
                className={cn(
                  "font-medium transition-colors hover:text-blue-600 relative py-2",
                  isActiveLink('/contact') ? "text-blue-600" : "text-gray-700"
                )}
              >
                Contact
                {isActiveLink('/contact') && (
                  <motion.div 
                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600"
                    layoutId="activeTab"
                  />
                )}
              </Link>
            </nav>

            {/* Search Bar */}
            <form onSubmit={submit} className="hidden md:flex items-center flex-1 max-w-md mx-8">
              <div className="relative w-full">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  value={q}
                  onChange={(e) => setQ(e.target.value)}
                  placeholder="Search products..."
                  className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50 hover:bg-white transition-colors"
                />
              </div>
            </form>

            {/* Right Actions */}
            <div className="flex items-center gap-4">
              
              {/* Wishlist (Desktop) */}
              <button className="hidden lg:flex items-center justify-center w-10 h-10 rounded-full hover:bg-gray-100 transition-colors relative">
                <Heart className="w-5 h-5 text-gray-600" />
              </button>

              {/* Cart */}
              <Link 
                to="/cart" 
                className="relative flex items-center justify-center w-10 h-10 rounded-full hover:bg-gray-100 transition-colors group"
              >
                <ShoppingBag className="w-5 h-5 text-gray-600 group-hover:text-blue-600 transition-colors" />
                {count > 0 && (
                  <motion.span 
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="absolute -top-1 -right-1 bg-blue-600 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center"
                  >
                    {count}
                  </motion.span>
                )}
              </Link>

              {/* Mobile Menu Button */}
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="lg:hidden flex items-center justify-center w-10 h-10 rounded-full hover:bg-gray-100 transition-colors"
              >
                {isMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
              </button>
            </div>
          </div>

          {/* Mobile Search */}
          <form onSubmit={submit} className="md:hidden mt-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                value={q}
                onChange={(e) => setQ(e.target.value)}
                placeholder="Search products..."
                className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50"
              />
            </div>
          </form>
        </div>
      </header>

      {/* Mobile Menu Overlay */}
      <AnimatePresence>
        {isMenuOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/50 z-40 lg:hidden"
              onClick={() => setIsMenuOpen(false)}
            />
            <motion.div
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'tween', duration: 0.3 }}
              className="fixed top-0 right-0 h-full w-80 bg-white z-50 lg:hidden shadow-xl"
            >
              <div className="p-6">
                <div className="flex items-center justify-between mb-8">
                  <span className="font-bold text-xl">Menu</span>
                  <button
                    onClick={() => setIsMenuOpen(false)}
                    className="w-8 h-8 rounded-full hover:bg-gray-100 flex items-center justify-center"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>

                <nav className="space-y-6">
                  <Link 
                    to="/shop" 
                    className="block text-lg font-medium text-gray-900 hover:text-blue-600 transition-colors"
                  >
                    Shop
                  </Link>
                  
                  <div>
                    <Link 
                      to="/categories" 
                      className="block text-lg font-medium text-gray-900 hover:text-blue-600 transition-colors mb-3"
                    >
                      Categories
                    </Link>
                    <div className="ml-4 space-y-2">
                      {categoriesLoading ? (
                        <div className="text-gray-500 text-sm">Loading...</div>
                      ) : (
                        categories.slice(0, 5).map((category) => {
                          const Icon = getCategoryIcon(category.key);
                          return (
                            <Link
                              key={category.key}
                              to={`/shop?category=${category.key}`}
                              className="flex items-center gap-2 text-gray-600 hover:text-blue-600 transition-colors"
                            >
                              <Icon className="w-4 h-4" />
                              <span>{category.label}</span>
                              {category.productCount > 0 && (
                                <span className="text-xs text-gray-400">
                                  ({category.productCount})
                                </span>
                              )}
                            </Link>
                          );
                        })
                      )}
                      {categories.length > 5 && (
                        <Link 
                          to="/categories" 
                          className="text-blue-600 text-sm hover:underline"
                        >
                          View all categories
                        </Link>
                      )}
                    </div>
                  </div>
                  
                  <Link 
                    to="/contact" 
                    className="block text-lg font-medium text-gray-900 hover:text-blue-600 transition-colors"
                  >
                    Contact
                  </Link>
                  
                  <div className="border-t border-gray-200 pt-6 space-y-4">
                    <button className="flex items-center gap-3 text-gray-700 hover:text-blue-600 transition-colors">
                      <Heart className="w-5 h-5" />
                      <span>Wishlist</span>
                    </button>
                  </div>
                </nav>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
