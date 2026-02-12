import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import cartService from '../services/cart.service';
import { handleGuestAdd, handleGuestUpdate, handleGuestRemove } from '../utils/cartHelpers';

const CartContext = createContext();
export const useCart = () => {
    const context = useContext(CartContext);
    if (!context) throw new Error('useCart must be used within a CartProvider');
    return context;
};

export const CartProvider = ({ children }) => {
    const [cartItems, setCartItems] = useState([]);
    const [loading, setLoading] = useState(false);
    const [isCartOpen, setIsCartOpen] = useState(false);
    const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));

    const loadCart = useCallback(async () => {
        if (!isLoggedIn) { const saved = localStorage.getItem('guest_cart'); if (saved) setCartItems(JSON.parse(saved)); return; }
        try { setLoading(true); const res = await cartService.getCart(); if (res.status === 'success') setCartItems(res.data.items || []); }
        catch (e) { console.error(e); } finally { setLoading(false); }
    }, [isLoggedIn]);

    useEffect(() => { loadCart(); }, [loadCart]);
    useEffect(() => { if (!isLoggedIn) localStorage.setItem('guest_cart', JSON.stringify(cartItems)); }, [cartItems, isLoggedIn]);

    const addToCart = async (p, v, q = 1) => {
        if (isLoggedIn) { try { if ((await cartService.addItem(v.id, q)).status === 'success') await loadCart(); } catch (e) { console.error(e); } }
        else { setCartItems(prev => handleGuestAdd(prev, p, v, q)); }
    };

    const updateQuantity = async (vid, q) => {
        if (q <= 0) return removeFromCart(vid);
        if (isLoggedIn) { try { await cartService.updateQuantity(vid, q); await loadCart(); } catch (e) { console.error(e); } }
        else { setCartItems(prev => handleGuestUpdate(prev, vid, q)); }
    };

    const removeFromCart = async (vid) => {
        if (isLoggedIn) { try { await cartService.removeItem(vid); await loadCart(); } catch (e) { console.error(e); } }
        else { setCartItems(prev => handleGuestRemove(prev, vid)); }
    };

    const clearCart = async () => {
        if (isLoggedIn) { try { await cartService.clearCart(); setCartItems([]); } catch (e) { console.error(e); } }
        else setCartItems([]);
    };

    const cartTotal = cartItems.reduce((t, i) => t + (i.price * i.quantity), 0);
    const cartCount = cartItems.reduce((c, i) => c + i.quantity, 0);

    return (
        <CartContext.Provider value={{ cartItems, loading, addToCart, updateQuantity, removeFromCart, clearCart, cartTotal, cartCount, isCartOpen, setIsCartOpen }}>
            {children}
        </CartContext.Provider>
    );
};
