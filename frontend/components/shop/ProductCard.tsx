import { Link } from 'react-router-dom';
import type { Product } from '../../data/products';
import { formatPrice } from '../../data/products';
import { useCart } from '../../context/cart';
import { getProductImageUrl } from '../../lib/media';

export default function ProductCard({ product }: { product: Product }) {
  const { add } = useCart();
  const isOutOfStock = product.is_in_stock === false || product.stock_quantity === 0;

  function onAdd(e: React.MouseEvent) {
    e.preventDefault();
    e.stopPropagation();
    if (!isOutOfStock) {
      add(product, 1);
    }
  }

  return (
    <Link
      to={`/product/${product.slug}`}
      className="group rounded-xl border bg-card hover:shadow-md transition overflow-hidden relative"
    >
      <div className="aspect-square overflow-hidden bg-muted relative">
        <img
          src={getProductImageUrl(product.image)}
          alt={product.title}
          className={`h-full w-full object-cover transition duration-300 group-hover:scale-105 ${
            isOutOfStock ? 'opacity-60 grayscale' : ''
          }`}
          loading="lazy"
        />
        {isOutOfStock && (
          <div className="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center">
            <span className="bg-red-600 text-white px-3 py-1 rounded-md text-sm font-medium">
              Out of Stock
            </span>
          </div>
        )}
        {!isOutOfStock && (
          <button
            onClick={onAdd}
            className="absolute right-3 bottom-3 rounded-md bg-[hsl(var(--brand-blue))] text-white px-3 py-1 text-sm font-medium shadow-lg opacity-95 hover:brightness-110"
          >
            Add
          </button>
        )}
      </div>
      <div className="p-4">
        <h3 className="font-medium line-clamp-1">{product.title}</h3>
        <div className="flex items-center justify-between mt-1">
          <p className="text-sm text-muted-foreground">{formatPrice(product.price)}</p>
          {product.stock_quantity !== undefined && (
            <p className={`text-xs ${isOutOfStock ? 'text-red-600' : 'text-green-600'}`}>
              {isOutOfStock ? 'Out of stock' : `${product.stock_quantity} in stock`}
            </p>
          )}
        </div>
      </div>
    </Link>
  );
}
