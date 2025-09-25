import { createContext, useContext, useEffect, useMemo, useReducer } from 'react';
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

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(reducer, initialState, () => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? (JSON.parse(raw) as State) : initialState;
    } catch {
      return initialState;
    }
  });

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }, [state]);

  const add = (p: Product, quantity?: number, selectedSize?: string, selectedColor?: string, variantId?: number) => {
    // Check if product is in stock before adding
    if (!p.is_in_stock || p.stock_quantity === 0) {
      console.warn(`Cannot add ${p.title} to cart: out of stock`);
      return;
    }
    
    // Check if requested quantity exceeds available stock
    const requestedQty = quantity || 1;
    if (p.stock_quantity < requestedQty) {
      console.warn(`Cannot add ${requestedQty} of ${p.title} to cart: only ${p.stock_quantity} in stock`);
      return;
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
      saveCheckoutData, getCheckoutData, clearCheckoutData 
    }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => useContext(CartContext);
