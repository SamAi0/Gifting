import { createContext, useState, useEffect, useCallback } from 'react';
import api from '../api';
import { useAuth } from './AuthContext';

export const CartContext = createContext();

export const CartProvider = ({ children }) => {
    const { token } = useAuth();
    const [cart, setCart] = useState(null);
    const [loading, setLoading] = useState(false);

    const fetchCart = useCallback(async () => {
        if (!token) {
            setCart(null);
            return;
        }
        setLoading(true);
        try {
            const res = await api.get('/orders/cart/');
            setCart(res.data);
        } catch (err) {
            console.error("Error fetching cart", err);
        } finally {
            setLoading(false);
        }
    }, [token]);

    // Fetch cart on mount and when token changes
    useEffect(() => {
        let isMounted = true;
        
        const syncCart = async () => {
            if (!token) {
                if (isMounted) {
                    setCart(null);
                }
                return;
            }
            
            setLoading(true);
            try {
                const res = await api.get('/orders/cart/');
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
    }, [token]);

    const addToCart = async (productId, quantity = 1, customizationText = '', customizationImage = null, customizationData = null, logoImage = null) => {
        if (!token) {
            alert("Please login to add items to cart");
            return;
        }
        
        const formData = new FormData();
        formData.append('product', productId);
        formData.append('quantity', quantity);
        if (customizationText) formData.append('customization_text', customizationText);
        if (customizationImage) formData.append('customization_image', customizationImage);
        if (customizationData) formData.append('customization_data', JSON.stringify(customizationData));
        if (logoImage) formData.append('logo_image', logoImage);

        try {
            await api.post('/orders/cart-items/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            fetchCart();
            alert("Added to cart!");
        } catch (err) {
            console.error("Error adding to cart", err);
        }
    };

    const removeFromCart = async (itemId) => {
        try {
            await api.delete(`/orders/cart-items/${itemId}/`);
            fetchCart();
        } catch (err) {
            console.error("Error removing from cart", err);
        }
    };

    const updateQuantity = async (itemId, quantity) => {
        try {
            await api.patch(`/orders/cart-items/${itemId}/`, { quantity });
            fetchCart();
        } catch (err) {
            console.error("Error updating quantity", err);
        }
    };

    return (
        <CartContext.Provider value={{ cart, loading, addToCart, removeFromCart, updateQuantity, fetchCart }}>
            {children}
        </CartContext.Provider>
    );
};

export { useCart } from './useCart';
