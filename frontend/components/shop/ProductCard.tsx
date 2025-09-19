import { Link } from 'react-router-dom';
import type { Product } from '../../data/products';
import { formatPrice } from '../../data/products';
import { useCart } from '../../context/cart';

export default function ProductCard({ product }: { product: Product }) {
  const { add } = useCart();

  function onAdd(e: React.MouseEvent) {
    e.preventDefault();
    e.stopPropagation();
    add(product, 1);
  }

  return (
    <Link
      to={`/product/${product.slug}`}
      className="group rounded-xl border bg-card hover:shadow-md transition overflow-hidden relative"
    >
      <div className="aspect-square overflow-hidden bg-muted">
        <img
          src={product.image}
          alt={product.title}
          className="h-full w-full object-cover transition duration-300 group-hover:scale-105"
          loading="lazy"
        />
        <button
          onClick={onAdd}
          className="absolute right-3 bottom-3 rounded-md bg-[hsl(var(--brand-blue))] text-white px-3 py-1 text-sm font-medium shadow-lg opacity-95 hover:brightness-110"
        >
          Add
        </button>
      </div>
      <div className="p-4">
        <h3 className="font-medium line-clamp-1">{product.title}</h3>
        <p className="mt-1 text-sm text-muted-foreground">{formatPrice(product.price)}</p>
      </div>
    </Link>
  );
}
