import { createContext, useState, useEffect, useCallback } from 'react';
import api from '../api';
import { useAuth } from './AuthContext';

export const CartContext = createContext();

export const CartProvider = ({ children }) => {
    const { user } = useAuth();
    const [cart, setCart] = useState(null);
    const [guestCart, setGuestCart] = useState(() => {
        const saved = localStorage.getItem('guest_cart');
        return saved ? JSON.parse(saved) : [];
    });
    const [loading, setLoading] = useState(false);

    // Save guest cart to local storage whenever it changes
    useEffect(() => {
        if (!user) {
            localStorage.setItem('guest_cart', JSON.stringify(guestCart));
        }
    }, [guestCart, user]);

    const fetchCart = useCallback(async () => {
        if (!user) {
            setCart(null);
            return;
        }
        setLoading(true);
        try {
            const res = await api.get('orders/cart/');
            setCart(res.data);
        } catch (err) {
            console.error("Error fetching cart", err);
        } finally {
            setLoading(false);
        }
    }, [user]);



    // Fetch cart on mount and when user changes
    useEffect(() => {
        let isMounted = true;
        
        const syncCart = async () => {
            if (!user) {
                if (isMounted) {
                    setCart(null);
                }
                return;
            }
            
            setLoading(true);
            try {
                // Check if there's a guest cart to merge
                const savedGuestCart = localStorage.getItem('guest_cart');
                if (savedGuestCart) {
                    const items = JSON.parse(savedGuestCart);
                    if (items.length > 0) {
                        await api.post('orders/merge-cart/', { items });
                        localStorage.removeItem('guest_cart');
                        setGuestCart([]);
                    }
                }
                
                const res = await api.get('orders/cart/');
                if (isMounted) {
                    setCart(res.data);
                }
            } catch (err) {
                console.error("Error fetching cart", err);
            } finally {
                if (isMounted) {
                    setLoading(false);
                }
            }
        };
        
        syncCart();
        
        return () => {
            isMounted = false;
        };
    }, [user]);

    const addToCart = async (productId, quantity = 1, customizationText = '', customizationImage = null, customizationData = null, logoImage = null) => {
        if (!user) {
            // Add to Guest Cart
            const newItem = {
                id: Date.now(), // Temporary ID
                product_id: productId,
                quantity,
                customization_text: customizationText,
                customization_data: customizationData,
                // Files can't be easily stored in localStorage, so we might skip them for guest cart
                // or just alert the user.
            };
            setGuestCart(prev => [...prev, newItem]);
            return;
        }
        
        const formData = new FormData();
        formData.append('product', productId);
        formData.append('quantity', quantity);
        if (customizationText) formData.append('customization_text', customizationText);
        if (customizationImage) formData.append('customization_image', customizationImage);
        if (customizationData) formData.append('customization_data', JSON.stringify(customizationData));
        if (logoImage) {
            if (Array.isArray(logoImage)) {
                logoImage.forEach((file) => {
                    formData.append('logo_image', file);
                });
            } else {
                formData.append('logo_image', logoImage);
            }
        }

        try {
            await api.post('orders/cart-items/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            fetchCart();
        } catch (err) {
            console.error("Error adding to cart", err);
        }
    };

    const removeFromCart = async (itemId) => {
        if (!user) {
            setGuestCart(prev => prev.filter(item => item.id !== itemId));
            return;
        }
        try {
            await api.delete(`orders/cart-items/${itemId}/`);
            fetchCart();
        } catch (err) {
            console.error("Error removing from cart", err);
        }
    };

    const updateQuantity = async (itemId, quantity) => {
        if (!user) {
            setGuestCart(prev => prev.map(item => item.id === itemId ? { ...item, quantity } : item));
            return;
        }
        try {
            await api.patch(`orders/cart-items/${itemId}/`, { quantity });
            fetchCart();
        } catch (err) {
            console.error("Error updating quantity", err);
        }
    };

    const cartToDisplay = user ? cart : { items: guestCart.map(item => ({
        ...item,
        subtotal: 0, // In guest mode we can't easily calculate subtotal without product data
        product: { id: item.product_id, name: 'Loading...' } // Placeholder
    })), total_price: 0 };

    return (
        <CartContext.Provider value={{ 
            cart: user ? cart : cartToDisplay, 
            guestCart,
            loading, 
            addToCart, 
            removeFromCart, 
            updateQuantity, 
            fetchCart 
        }}>
            {children}
        </CartContext.Provider>
    );
};

export { useCart } from './useCart';
