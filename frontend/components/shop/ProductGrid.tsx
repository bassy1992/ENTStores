import ProductCard from './ProductCard';
import type { Product } from '../../data/products';

export default function ProductGrid({ products }: { products: Product[] }) {
  return (
    <div className="grid gap-6 grid-cols-2 sm:grid-cols-3 lg:grid-cols-4">
      {products.map((p) => (
        <ProductCard key={p.id} product={p} />
      ))}
    </div>
  );
}
