import { categories } from '../../data/products';
import { Link } from 'react-router-dom';
import { 
  Mail, 
  Phone, 
  MapPin, 
  Facebook, 
  Twitter, 
  Instagram, 
  Youtube,
  Shield,
  Truck,
  RefreshCw,
  CreditCard,
  ArrowRight,
  Heart
} from 'lucide-react';
import { useState } from 'react';

export default function Footer() {
  const [email, setEmail] = useState('');
  const [subscribed, setSubscribed] = useState(false);

  const handleSubscribe = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      setSubscribed(true);
      setEmail('');
      setTimeout(() => setSubscribed(false), 3000);
    }
  };

  return (
    <footer className="bg-gray-900 text-white mt-16">
      {/* Main Footer Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Brand Section */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <img 
                src="https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fa7419136808a40ba94992db25a691b96?format=webp&width=120" 
                alt="ENNC logo" 
                className="h-5 w-auto" 
              />
              <span className="text-lg font-bold">ENNC</span>
            </div>
            <p className="text-gray-300 text-sm mb-3">
              Elevated streetwear for the modern lifestyle.
            </p>
            
            {/* Social Media */}
            <div className="flex gap-2">
              {[
                { icon: Facebook, href: '#', label: 'Facebook' },
                { icon: Twitter, href: '#', label: 'Twitter' },
                { icon: Instagram, href: '#', label: 'Instagram' }
              ].map(({ icon: Icon, href, label }) => (
                <a
                  key={label}
                  href={href}
                  className="w-7 h-7 bg-gray-800 rounded-full flex items-center justify-center hover:bg-blue-600 transition-colors"
                  aria-label={label}
                >
                  <Icon className="w-3 h-3" />
                </a>
              ))}
            </div>
          </div>

          {/* Links Section */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <h4 className="font-semibold mb-3 text-sm">Shop</h4>
              <ul className="space-y-1 text-sm">
                <li>
                  <Link to="/shop" className="text-gray-300 hover:text-white transition-colors">
                    All Products
                  </Link>
                </li>
                <li>
                  <Link to="/categories" className="text-gray-300 hover:text-white transition-colors">
                    Categories
                  </Link>
                </li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-3 text-sm">Support</h4>
              <ul className="space-y-1 text-sm">
                <li>
                  <Link to="/contact" className="text-gray-300 hover:text-white transition-colors">
                    Contact
                  </Link>
                </li>
                <li>
                  <a href="#shipping" className="text-gray-300 hover:text-white transition-colors">
                    Shipping
                  </a>
                </li>
              </ul>
            </div>
          </div>

          {/* Newsletter */}
          <div>
            <h4 className="font-semibold mb-3 text-sm">Newsletter</h4>
            <form onSubmit={handleSubscribe} className="flex gap-2">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Your email"
                className="flex-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded text-white placeholder-gray-400 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                required
              />
              <button
                type="submit"
                className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded text-sm transition-colors"
              >
                {subscribed ? '✓' : 'Join'}
              </button>
            </form>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-gray-800">
        <div className="max-w-7xl mx-auto px-4 py-3">
          <div className="flex flex-col md:flex-row justify-between items-center gap-2 text-xs text-gray-400">
            <div className="flex items-center gap-4">
              <p>© {new Date().getFullYear()} ENNC. All rights reserved.</p>
              <div className="flex gap-3">
                <a href="#privacy" className="hover:text-white transition-colors">Privacy</a>
                <a href="#terms" className="hover:text-white transition-colors">Terms</a>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <Shield className="w-3 h-3 text-blue-400" />
              <span>Secure</span>
              <span>•</span>
              <Truck className="w-3 h-3 text-blue-400" />
              <span>Free shipping $75+</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
