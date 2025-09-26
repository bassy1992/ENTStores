export type Category =
  | 't-shirts'
  | 'polos'
  | 'hoodies'
  | 'sweatshirts'
  | 'tracksuits'
  | 'jackets'
  | 'shorts'
  | 'headwear'
  | 'accessories';

export type Product = {
  id: string;
  title: string;
  slug: string;
  price: number; // in cents
  shipping_cost?: number; // in dollars
  description: string;
  image: string;
  category: Category;
  tags?: string[];
  stock_quantity?: number;
  is_in_stock?: boolean;
  average_rating?: number;
  total_reviews?: number;
  variants?: any[]; // For product variants
};

// Lightweight, extendable in-memory catalog. In a real app fetch from API/DB.
export const products: Product[] = [
  {
    id: 'track-jacket-sky',
    title: 'ENNC Track Jacket — Sky',
    slug: 'ennc-track-jacket-sky',
    price: 7500,
    description: 'Lightweight track jacket with signature ENNC chest script and retro paneling. Comfortable fit and durable zipper.',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F690488dfe67548ada8fe07090b86601f?format=webp&width=800',
    category: 'tracksuits',
    tags: ['featured', 'new'],
  },
  {
    id: 'track-jacket-olive',
    title: 'ENNC Track Jacket — Olive',
    slug: 'ennc-track-jacket-olive',
    price: 7500,
    description: 'ENNC retro-inspired track jacket in olive tones. Durable construction with branded sleeve tab.',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F0c4ab9be3dd740618a71b6809f4d5f28?format=webp&width=800',
    category: 'tracksuits',
    tags: ['featured'],
  },
  {
    id: 'tee-classic-black',
    title: 'Classic Logo Tee — Black',
    slug: 'classic-logo-tee-black',
    price: 2800,
    description:
      'Ultra-soft cotton tee with premium screen print. Tailored athletic fit and reinforced collar for daily wear.',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fa03929e1731e4efcadc34cef66af98ba?format=webp&width=800',
    category: 't-shirts',
    tags: ['new'],
  },
  {
    id: 'tee-classic-white',
    title: 'Classic Logo Tee — White',
    slug: 'classic-logo-tee-white',
    price: 2800,
    description:
      'Signature logo on breathable mid‑weight cotton. Clean look that pairs with anything.',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Ff6d93005cb0342e0ae5980da9f131c00?format=webp&width=800',
    category: 't-shirts',
    tags: ['bestseller'],
  },
  {
    id: 'cap-snapback',
    title: 'Heritage Snapback Cap',
    slug: 'heritage-snapback-cap',
    price: 3200,
    description:
      'Structured 6‑panel snapback with curved brim, moisture-wicking band, and raised embroidery.',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fde3830a62f2e4e32b3e515795bd471cf?format=webp&width=800',
    category: 'headwear',
  },
  {
    id: 'duffel-weekender',
    title: 'City Weekender Duffel',
    slug: 'city-weekender-duffel',
    price: 8900,
    description:
      'Durable canvas duffel with water-repellent coating, metal hardware, and removable shoulder strap.',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F7e980c238ab54fb5893ffdd1999f2c37?format=webp&width=800',
    category: 'accessories',
  },
  {
    id: 'socks-comfort',
    title: 'Comfort Crew Socks (2‑Pack)',
    slug: 'comfort-crew-socks',
    price: 1600,
    description:
      'Breathable cotton blend with arch support and cushioned sole for all‑day comfort.',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Ff6d93005cb0342e0ae5980da9f131c00?format=webp&width=800',
    category: 'accessories',
  },
  {
    id: 'polo-navy',
    title: 'Classic Polo — Navy',
    slug: 'classic-polo-navy',
    price: 4200,
    description: 'Premium pique cotton polo with mother-of-pearl buttons and embroidered logo.',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F65c976a3ea2e4593b4d1a27829d0f390?format=webp&width=800',
    category: 'polos',
    tags: ['new'],
  },
  {
    id: 'hoodie-grey',
    title: 'Essential Hoodie — Grey',
    slug: 'essential-hoodie-grey',
    price: 6500,
    description: 'Heavyweight cotton hoodie with kangaroo pocket and adjustable drawstring hood.',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F7e980c238ab54fb5893ffdd1999f2c37?format=webp&width=800',
    category: 'hoodies',
    tags: ['featured', 'bestseller'],
  },
  {
    id: 'sweatshirt-cream',
    title: 'Crewneck Sweatshirt — Cream',
    slug: 'crewneck-sweatshirt-cream',
    price: 5800,
    description: 'Soft fleece-lined sweatshirt with ribbed cuffs and hem for a comfortable fit.',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fa03929e1731e4efcadc34cef66af98ba?format=webp&width=800',
    category: 'sweatshirts',
  },
  {
    id: 'jacket-bomber',
    title: 'Bomber Jacket — Black',
    slug: 'bomber-jacket-black',
    price: 8900,
    description: 'Classic bomber jacket with ribbed collar, cuffs, and hem. Water-resistant outer shell.',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F0c4ab9be3dd740618a71b6809f4d5f28?format=webp&width=800',
    category: 'jackets',
    tags: ['featured'],
  },
  {
    id: 'shorts-athletic',
    title: 'Athletic Shorts — Navy',
    slug: 'athletic-shorts-navy',
    price: 3800,
    description: 'Lightweight athletic shorts with moisture-wicking fabric and side pockets.',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F690488dfe67548ada8fe07090b86601f?format=webp&width=800',
    category: 'shorts',
  },
  {
    id: 'beanie-wool',
    title: 'Wool Beanie — Charcoal',
    slug: 'wool-beanie-charcoal',
    price: 2400,
    description: 'Soft merino wool beanie with fold-over cuff and embroidered logo patch.',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fde3830a62f2e4e32b3e515795bd471cf?format=webp&width=800',
    category: 'headwear',
    tags: ['new'],
  },
];

export type CategoryModel = {
  key: Category;
  label: string;
  description: string;
  image: string;
  featured?: boolean;
  productCount?: number;
};

export const categories: { key: Category; label: string }[] = [
  { key: 't-shirts', label: 'T shirts' },
  { key: 'polos', label: 'Polos' },
  { key: 'hoodies', label: 'Hoodies / crewnecks' },
  { key: 'sweatshirts', label: 'Sweatshirt' },
  { key: 'tracksuits', label: 'Tracksuits' },
  { key: 'jackets', label: 'Jackets' },
  { key: 'shorts', label: 'Shorts' },
  { key: 'headwear', label: 'Headwear' },
  { key: 'accessories', label: 'Accessories' },
];

export const categoryModels: CategoryModel[] = [
  {
    key: 't-shirts',
    label: 'T-Shirts',
    description: 'Premium cotton tees with signature designs and comfortable fits',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fa03929e1731e4efcadc34cef66af98ba?format=webp&width=600',
    featured: true,
    productCount: 12
  },
  {
    key: 'polos',
    label: 'Polos',
    description: 'Classic polo shirts for smart-casual occasions',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Ff6d93005cb0342e0ae5980da9f131c00?format=webp&width=600',
    featured: false,
    productCount: 8
  },
  {
    key: 'hoodies',
    label: 'Hoodies / Crewnecks',
    description: 'Cozy hoodies and crewnecks for everyday comfort',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F65c976a3ea2e4593b4d1a27829d0f390?format=webp&width=600',
    featured: true,
    productCount: 15
  },
  {
    key: 'sweatshirts',
    label: 'Sweatshirts',
    description: 'Warm and stylish sweatshirts for cooler days',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F7e980c238ab54fb5893ffdd1999f2c37?format=webp&width=600',
    featured: false,
    productCount: 10
  },
  {
    key: 'tracksuits',
    label: 'Tracksuits',
    description: 'Athletic tracksuits for sport and street style',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F690488dfe67548ada8fe07090b86601f?format=webp&width=600',
    featured: true,
    productCount: 6
  },
  {
    key: 'jackets',
    label: 'Jackets',
    description: 'Versatile jackets for all seasons and occasions',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F0c4ab9be3dd740618a71b6809f4d5f28?format=webp&width=600',
    featured: false,
    productCount: 9
  },
  {
    key: 'shorts',
    label: 'Shorts',
    description: 'Comfortable shorts for active lifestyles',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fa03929e1731e4efcadc34cef66af98ba?format=webp&width=600',
    featured: false,
    productCount: 7
  },
  {
    key: 'headwear',
    label: 'Headwear',
    description: 'Caps, beanies, and hats to complete your look',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fde3830a62f2e4e32b3e515795bd471cf?format=webp&width=600',
    featured: true,
    productCount: 11
  },
  {
    key: 'accessories',
    label: 'Accessories',
    description: 'Bags, socks, and essential accessories',
    image: 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F7e980c238ab54fb5893ffdd1999f2c37?format=webp&width=600',
    featured: false,
    productCount: 14
  }
];

export const formatPrice = (price: number) => {
  // Backend is sending prices in dollars (not cents)
  // So we format directly without dividing by 100
  return new Intl.NumberFormat('en-US', { 
    style: 'currency', 
    currency: 'USD' 
  }).format(price);
};
