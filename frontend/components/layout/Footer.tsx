import { categories } from '../../data/products';

export default function Footer() {
  return (
    <footer className="mt-16 border-t">
      <div className="container mx-auto px-4 py-10 grid gap-8 md:grid-cols-4 text-sm text-foreground/80">
        <div>
          <div className="flex items-center gap-2">
            <img src="https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fa7419136808a40ba94992db25a691b96?format=webp&width=120" alt="ENNC logo" className="h-6 w-auto" />
            <span className="font-bold">ENNC</span>
          </div>
          <p className="mt-3 max-w-xs">Loyalty. Love. Respect. Streetwear engineered for everyday performance.</p>
        </div>
        <div>
          <p className="font-semibold text-foreground">Shop</p>
          <ul className="mt-3 space-y-2">
            <li><a href="/shop" className="hover:text-foreground">All products</a></li>
            {categories.slice(0,4).map((c) => (
              <li key={c.key}><a href={`/shop?c=${encodeURIComponent(c.key)}`} className="hover:text-foreground">{c.label}</a></li>
            ))}
          </ul>
        </div>
        <div>
          <p className="font-semibold text-foreground">Help</p>
          <ul className="mt-3 space-y-2">
            <li><a href="/contact" className="hover:text-foreground">Customer support</a></li>
            <li><a href="#help" className="hover:text-foreground">Shipping & returns</a></li>
            <li><a href="#help" className="hover:text-foreground">FAQ</a></li>
          </ul>
        </div>
        <div>
          <p className="font-semibold text-foreground">Stay updated</p>
          <form className="mt-3 flex">
            <input className="w-full rounded-l-md border px-3 py-2" placeholder="Email address" />
            <button className="rounded-r-md bg-foreground text-background px-4">Join</button>
          </form>
        </div>
      </div>
      <div className="border-t py-4 text-center text-xs text-foreground/60">© {new Date().getFullYear()} ENNC. All rights reserved.</div>
    </footer>
  );
}
