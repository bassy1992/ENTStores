import { createContext, useContext, useEffect, useMemo, useReducer, useState } from 'react';
import type { Product } from '../data/products';

export type CartItem = {
  id: string; // product id
  title: string;
  price: number; // cents
  image: string;
  quantity: number;
  selectedSize?: string;
  selectedColor?: string;
  variantId?: number;
  uniqueKey?: string; // For distinguishing same product with different variants
};

type State = {
  items: CartItem[];
};

type Action =
  | { type: 'ADD'; product: Product; quantity?: number; selectedSize?: string; selectedColor?: string; variantId?: number }
  | { type: 'REMOVE'; uniqueKey: string }
  | { type: 'SET_QTY'; uniqueKey: string; quantity: number }
  | { type: 'CLEAR' };

const initialState: State = { items: [] };

const CartContext = createContext<{
  state: State;
  add: (p: Product, quantity?: number, selectedSize?: string, selectedColor?: string, variantId?: number) => void;
  remove: (uniqueKey: string) => void;
  setQty: (uniqueKey: string, qty: number) => void;
  clear: () => void;
  count: number;
  subtotal: number; // cents
  saveCheckoutData: (data: any) => void;
  getCheckoutData: () => any;
  clearCheckoutData: () => void;
  appliedPromoCode: any;
  setAppliedPromoCode: (promoCode: any) => void;
}>({
  state: initialState,
  add: () => {},
  remove: () => {},
  setQty: () => {},
  clear: () => {},
  count: 0,
  subtotal: 0,
  saveCheckoutData: () => {},
  getCheckoutData: () => null,
  clearCheckoutData: () => {},
  appliedPromoCode: null,
  setAppliedPromoCode: () => {},
});

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'ADD': {
      const qty = action.quantity ?? 1;
      
      // Create unique key for this product variant combination
      const uniqueKey = `${action.product.id}-${action.selectedSize || 'no-size'}-${action.selectedColor || 'no-color'}`;
      
      const existing = state.items.find((i) => i.uniqueKey === uniqueKey);
      if (existing) {
        return {
          items: state.items.map((i) =>
            i.uniqueKey === uniqueKey ? { ...i, quantity: i.quantity + qty } : i,
          ),
        };
      }
      
      return {
        items: [
          ...state.items,
          {
            id: action.product.id,
            title: action.product.title,
            price: action.product.price,
            image: action.product.image,
            quantity: qty,
            selectedSize: action.selectedSize,
            selectedColor: action.selectedColor,
            variantId: action.variantId,
            uniqueKey,
          },
        ],
      };
    }
    case 'REMOVE':
      return { items: state.items.filter((i) => i.uniqueKey !== action.uniqueKey) };
    case 'SET_QTY':
      return {
        items: state.items
          .map((i) => (i.uniqueKey === action.uniqueKey ? { ...i, quantity: action.quantity } : i))
          .filter((i) => i.quantity > 0),
      };
    case 'CLEAR':
      return { items: [] };
    default:
      return state;
  }
}

const STORAGE_KEY = 'ennc_cart_v1';
const CHECKOUT_DATA_KEY = 'ennc_checkout_data_v1';
const PROMO_CODE_KEY = 'ennc_promo_code_v1';

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(reducer, initialState, () => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? (JSON.parse(raw) as State) : initialState;
    } catch {
      return initialState;
    }
  });

  const [appliedPromoCode, setAppliedPromoCodeState] = useState<any>(() => {
    try {
      const raw = localStorage.getItem(PROMO_CODE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  });

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }, [state]);

  useEffect(() => {
    if (appliedPromoCode) {
      localStorage.setItem(PROMO_CODE_KEY, JSON.stringify(appliedPromoCode));
    } else {
      localStorage.removeItem(PROMO_CODE_KEY);
    }
  }, [appliedPromoCode]);

  const setAppliedPromoCode = (promoCode: any) => {
    setAppliedPromoCodeState(promoCode);
  };

  const add = (p: Product, quantity?: number, selectedSize?: string, selectedColor?: string, variantId?: number) => {
    const requestedQty = quantity || 1;
    
    // If a variant is specified, validate variant stock
    if (variantId && p.variants) {
      const variant = p.variants.find(v => v.id === variantId);
      if (!variant) {
        console.warn(`Cannot add ${p.title} to cart: variant not found`);
        return;
      }
      if (!variant.is_in_stock || variant.stock_quantity === 0) {
        console.warn(`Cannot add ${p.title} to cart: selected variant is out of stock`);
        return;
      }
      if (variant.stock_quantity < requestedQty) {
        console.warn(`Cannot add ${requestedQty} of ${p.title} to cart: only ${variant.stock_quantity} in stock for selected variant`);
        return;
      }
    } else {
      // For products without variants or when no variant is selected
      if (!p.is_in_stock) {
        console.warn(`Cannot add ${p.title} to cart: out of stock`);
        return;
      }
      
      // If product has variants but no variant is selected, require variant selection
      if (p.variants && p.variants.length > 0) {
        console.warn(`Cannot add ${p.title} to cart: please select size and color options`);
        return;
      }
      
      // Check main product stock for products without variants
      if (p.stock_quantity < requestedQty) {
        console.warn(`Cannot add ${requestedQty} of ${p.title} to cart: only ${p.stock_quantity} in stock`);
        return;
      }
    }
    
    dispatch({ type: 'ADD', product: p, quantity, selectedSize, selectedColor, variantId });
  };
  const remove = (uniqueKey: string) => dispatch({ type: 'REMOVE', uniqueKey });
  const setQty = (uniqueKey: string, quantity: number) => dispatch({ type: 'SET_QTY', uniqueKey, quantity });
  const clear = () => dispatch({ type: 'CLEAR' });

  const saveCheckoutData = (data: any) => {
    try {
      localStorage.setItem(CHECKOUT_DATA_KEY, JSON.stringify(data));
    } catch (error) {
      console.error('Failed to save checkout data:', error);
    }
  };

  const getCheckoutData = () => {
    try {
      const data = localStorage.getItem(CHECKOUT_DATA_KEY);
      return data ? JSON.parse(data) : null;
    } catch (error) {
      console.error('Failed to get checkout data:', error);
      return null;
    }
  };

  const clearCheckoutData = () => {
    try {
      localStorage.removeItem(CHECKOUT_DATA_KEY);
    } catch (error) {
      console.error('Failed to clear checkout data:', error);
    }
  };

  const { count, subtotal } = useMemo(() => {
    const c = state.items.reduce((n, i) => n + i.quantity, 0);
    const s = state.items.reduce((n, i) => n + i.price * i.quantity, 0);
    return { count: c, subtotal: s };
  }, [state.items]);

  return (
    <CartContext.Provider value={{ 
      state, add, remove, setQty, clear, count, subtotal,
      saveCheckoutData, getCheckoutData, clearCheckoutData,
      appliedPromoCode, setAppliedPromoCode
    }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => useContext(CartContext);
