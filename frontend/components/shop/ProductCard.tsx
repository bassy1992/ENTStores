import { Link } from 'react-router-dom';
import type { Product } from '../../data/products';
import { formatPrice } from '../../data/products';
import { useCart } from '../../context/cart';
import { getProductImageUrl } from '../../lib/media';

export default function ProductCard({ product }: { product: Product }) {
  const { add } = useCart();
  
  // Check if product is truly out of stock
  // For products with variants, use is_in_stock (which considers variant availability)
  // For products without variants, check both is_in_stock and stock_quantity
  const hasVariants = product.variants && product.variants.length > 0;
  const isOutOfStock = hasVariants 
    ? product.is_in_stock === false 
    : (product.is_in_stock === false || product.stock_quantity === 0);
  
  // For products with variants, don't allow direct add to cart from grid
  const canAddDirectly = !hasVariants && !isOutOfStock;

  function onAdd(e: React.MouseEvent) {
    e.preventDefault();
    e.stopPropagation();
    if (canAddDirectly) {
      add(product, 1);
    }
  }

  function handleCardClick(e: React.MouseEvent) {
    // Prevent navigation if product is truly out of stock
    if (isOutOfStock) {
      e.preventDefault();
      e.stopPropagation();
      return;
    }
  }

  // Use div instead of Link for out of stock products
  const CardWrapper = isOutOfStock ? 'div' : Link;
  const cardProps = isOutOfStock 
    ? { 
        className: "group rounded-xl border bg-card transition overflow-hidden relative cursor-not-allowed opacity-75",
        onClick: handleCardClick
      }
    : { 
        to: `/product/${product.slug}`,
        className: "group rounded-xl border bg-card hover:shadow-md transition overflow-hidden relative"
      };

  return (
    <CardWrapper {...cardProps}>
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
            {hasVariants ? 'Options' : 'Add'}
          </button>
        )}
      </div>
      <div className="p-4">
        <h3 className="font-medium line-clamp-1">{product.title}</h3>
        <div className="flex items-center justify-between mt-1">
          <p className="text-sm text-muted-foreground">{formatPrice(product.price)}</p>
          {product.stock_quantity !== undefined && (
            <p className={`text-xs ${isOutOfStock ? 'text-red-600' : 'text-green-600'}`}>
              {isOutOfStock 
                ? 'Out of stock' 
                : hasVariants 
                  ? 'Multiple options'
                  : `${product.stock_quantity} in stock`
              }
            </p>
          )}
        </div>
      </div>
    </CardWrapper>
  );
}
