import { Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { useCart } from '../../context/cart';
import { cn } from '../../lib/utils';

export default function Header() {
  const { count } = useCart();
  const [q, setQ] = useState('');
  const navigate = useNavigate();

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    const query = q.trim();
    if (query) navigate(`/search?q=${encodeURIComponent(query)}`);
  };

  return (
    <header className="sticky top-0 z-50 backdrop-blur bg-white/70 dark:bg-black/40 border-b border-border">
      <div className="container mx-auto px-4 py-3 flex items-center gap-4">
        <Link to="/" className="flex items-center gap-3">
          <img src="https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fa7419136808a40ba94992db25a691b96?format=webp&width=200" alt="ENNC logo" className="h-8 w-auto" />
          <span className="font-extrabold tracking-tight text-lg">ENNC</span>
        </Link>

        <nav className="ml-6 hidden md:flex items-center gap-6 text-sm font-medium text-foreground/80">
          <Link to="/shop" className="hover:text-foreground">Shop</Link>
          <Link to="/categories" className="hover:text-foreground">Categories</Link>
          <Link to="/contact" className="hover:text-foreground">Contact</Link>
          <a href="#help" className="hover:text-foreground">Help</a>
        </nav>

        <form onSubmit={submit} className="ml-auto flex-1 max-w-lg hidden sm:flex items-center">
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Search products..."
            className={cn(
              'w-full rounded-l-md border border-r-0 bg-background px-3 py-2 outline-none focus:ring-2',
              'focus:ring-[hsl(var(--brand-blue))]'
            )}
          />
          <button
            type="submit"
            className="rounded-r-md bg-[hsl(var(--brand-blue))] text-white px-4 py-2 font-medium hover:brightness-110"
          >
            Search
          </button>
        </form>

        <Link to="/cart" className="relative rounded-md px-3 py-2 font-medium bg-secondary hover:bg-secondary/80">
          Cart
          {count > 0 && (
            <span className="absolute -top-2 -right-2 text-xs h-5 min-w-[1.25rem] grid place-items-center rounded-full bg-[hsl(var(--brand-red))] text-white px-1">
              {count}
            </span>
          )}
        </Link>
      </div>
    </header>
  );
}
