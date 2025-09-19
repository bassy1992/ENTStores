import { Link, useLocation } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { apiService, convertApiCategory, type ApiCategory } from '../../services/api';

export default function CategoryPills() {
  const { search } = useLocation();
  const params = new URLSearchParams(search);
  const active = params.get('c');
  
  const [categories, setCategories] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const apiCategories = await apiService.getCategories();
        const convertedCategories = apiCategories.map(convertApiCategory);
        setCategories(convertedCategories);
      } catch (err) {
        console.error('Failed to fetch categories:', err);
        // Fallback to empty array if API fails
        setCategories([]);
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, []);

  if (loading) {
    return (
      <div className="flex flex-wrap gap-2">
        <div className="px-3 py-1.5 rounded-full border bg-gray-200 animate-pulse">All</div>
        {[...Array(6)].map((_, i) => (
          <div key={i} className="px-3 py-1.5 rounded-full border bg-gray-200 animate-pulse w-20 h-8"></div>
        ))}
      </div>
    );
  }

  return (
    <div className="flex flex-wrap gap-2">
      <Link
        to="/shop"
        className={`px-3 py-1.5 rounded-full border transition-colors ${!active ? 'bg-foreground text-background' : 'hover:border-foreground'}`}
      >
        All
      </Link>
      {categories.map((c) => (
        <Link
          key={c.key}
          to={`/shop?c=${encodeURIComponent(c.key)}`}
          className={`px-3 py-1.5 rounded-full border hover:border-foreground transition-colors ${active === c.key ? 'bg-foreground text-background' : ''}`}
        >
          {c.label}
        </Link>
      ))}
    </div>
  );
}
