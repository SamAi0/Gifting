import { createContext, useState, useEffect, useCallback } from 'react';
import api from '../api';
import { useAuth } from './AuthContext';

export const CartContext = createContext();

export const CartProvider = ({ children }) => {
    const { user } = useAuth();
    const [cart, setCart] = useState(null);
    const [loading, setLoading] = useState(false);
    const [savedItems, setSavedItems] = useState([]);
    
    // Guest Session Management
    const [sessionId] = useState(() => {
        let sid = localStorage.getItem('cart_session_id');
        if (!sid) {
            sid = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
            localStorage.setItem('cart_session_id', sid);
        }
        return sid;
    });

    const fetchCart = useCallback(async (isMounted = { current: true }) => {
        setLoading(true);
        try {
            const url = user ? 'orders/cart/' : `orders/cart/?session_id=${sessionId}`;
            const res = await api.get(url);
            if (isMounted.current) {
                setCart(res.data);
            }
            
            // Also fetch saved items
            const savedUrl = user ? 'orders/save-for-later/' : `orders/save-for-later/?session_id=${sessionId}`;
            const savedRes = await api.get(savedUrl);
            if (isMounted.current) {
                setSavedItems(savedRes.data.results || savedRes.data);
            }
        } catch (err) {
            console.error("Error fetching cart", err);
        } finally {
            if (isMounted.current) {
                setLoading(false);
            }
        }
    }, [user, sessionId]);

    const mergeGuestCart = useCallback(async () => {
        if (!user || !sessionId) return;
        try {
            // Using the session_id approach on backend is cleaner
            await api.post('orders/merge-cart/', { session_id: sessionId });
            // After merge, clear local session if desired, or just re-fetch
            // For now, we'll just re-fetch to get the combined cart
            fetchCart();
        } catch (err) {
            console.error("Error merging guest cart", err);
        }
    }, [user, sessionId, fetchCart]);

    // Automatically merge cart when user logs in
    useEffect(() => {
        if (user && sessionId) {
            const hasGuestItems = localStorage.getItem('cart_session_id'); // Just a check
            if (hasGuestItems) {
                const runMerge = async () => {
                    await mergeGuestCart();
                };
                runMerge();
            }
        }
    }, [user, sessionId, mergeGuestCart]);

    // Fetch cart on mount and when user changes
    useEffect(() => {
        const isMounted = { current: true };
        
        const runFetch = async () => {
            await fetchCart(isMounted);
        };
        runFetch();
        
        return () => {
            isMounted.current = false;
        };
    }, [fetchCart]);

    const addToCart = async (productId, quantity = 1, customizationText = '', customizationImage = null, customizationData = null, logoImage = null) => {
        const formData = new FormData();
        formData.append('product', productId);
        formData.append('quantity', quantity);
        if (customizationText) formData.append('customization_text', customizationText);
        if (customizationImage) formData.append('customization_image', customizationImage);
        if (customizationData) formData.append('customization_data', JSON.stringify(customizationData));
        
        if (logoImage) {
            if (Array.isArray(logoImage)) {
                logoImage.forEach((file) => formData.append('logo_image', file));
            } else {
                formData.append('logo_image', logoImage);
            }
        }

        try {
            const url = `orders/cart-items/${user ? '' : `?session_id=${sessionId}`}`;
            await api.post(url, formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            fetchCart();
        } catch (err) {
            console.error("Error adding to cart", err);
        }
    };

    const removeFromCart = async (itemId) => {
        try {
            const url = `orders/cart-items/${itemId}/${user ? '' : `?session_id=${sessionId}`}`;
            await api.delete(url);
            fetchCart();
        } catch (err) {
            console.error("Error removing from cart", err);
        }
    };

    const updateQuantity = async (itemId, quantity) => {
        try {
            const url = `orders/cart-items/${itemId}/${user ? '' : `?session_id=${sessionId}`}`;
            await api.patch(url, { quantity });
            fetchCart();
        } catch (err) {
            console.error("Error updating quantity", err);
        }
    };

    const saveForLater = async (itemId) => {
        try {
            const url = `orders/cart-items/${itemId}/save_for_later/${user ? '' : `?session_id=${sessionId}`}`;
            await api.post(url);
            fetchCart();
        } catch (err) {
            console.error("Error saving for later", err);
        }
    };

    const moveToCart = async (savedItemId) => {
        try {
            const url = `orders/save-for-later/${savedItemId}/move_to_cart/${user ? '' : `?session_id=${sessionId}`}`;
            await api.post(url);
            fetchCart();
        } catch (err) {
            console.error("Error moving to cart", err);
        }
    };

    return (
        <CartContext.Provider value={{ 
            cart, 
            savedItems,
            loading, 
            addToCart, 
            removeFromCart, 
            updateQuantity, 
            saveForLater,
            moveToCart,
            fetchCart,
            mergeGuestCart
        }}>
            {children}
        </CartContext.Provider>
    );
};

export { useCart } from './useCart';
