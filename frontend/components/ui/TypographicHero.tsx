import { Link } from 'react-router-dom';

export default function TypographicHero({ images }: { images: string[] }) {
  // Use first image as product showcase; no background image
  const product = images && images.length > 0 ? images[0] : undefined;

  return (
    <section aria-label="Hero" className="w-full bg-white">
      <div className="max-w-7xl mx-auto px-4 py-20 lg:py-28">
        <div className="grid grid-cols-1 lg:grid-cols-12 items-center gap-8">
          <div className="lg:col-span-7 text-center lg:text-left">
            <p className="inline-flex items-center gap-2 rounded-full bg-[hsl(var(--brand-blue))]/10 px-3 py-1 text-xs text-foreground/80">New drop just landed</p>

            <h1 className="mt-6 text-4xl sm:text-5xl lg:text-6xl font-extrabold leading-tight tracking-tight">
              <span className="block bg-clip-text text-transparent bg-gradient-to-r from-[hsl(var(--brand-red))] to-[hsl(var(--brand-blue))]">ENNC — Elevated streetwear</span>
            </h1>

            <p className="mt-4 text-lg text-muted-foreground max-w-xl">
              Signature pieces built for daily wear — premium materials, clean silhouettes, and bold branding. Shop the latest drop curated for movement and comfort.
            </p>

            <div className="mt-8 flex flex-col sm:flex-row sm:items-center gap-3 justify-center lg:justify-start">
              <Link to="/shop" className="inline-block rounded-md bg-[hsl(var(--brand-blue))] text-white px-6 py-3 font-semibold">Shop the drop</Link>
              <Link to="/contact" className="inline-block rounded-md border border-border text-foreground px-6 py-3 font-medium">Get support</Link>
            </div>

            <div className="mt-6 text-sm text-muted-foreground">
              Free shipping over $75 • 30‑day returns
            </div>
          </div>

          <div className="lg:col-span-5 flex items-center justify-center lg:justify-end">
            {product ? (
              <div className="relative w-[300px] sm:w-[360px] lg:w-[420px]">
                <div className="rounded-2xl overflow-hidden shadow-xl border">
                  <img src={product} alt="product" className="w-full h-auto object-cover block" />
                </div>
                <div className="absolute -right-4 -bottom-4 rounded-xl px-3 py-1 bg-[hsl(var(--brand-red))] text-white text-xs font-semibold shadow">Limited run</div>
              </div>
            ) : null}
          </div>
        </div>
      </div>
    </section>
  );
}
