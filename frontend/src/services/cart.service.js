import api from './api';

const cartService = {
    getCart: async () => {
        const response = await api.get('/cart');
        return response.data;
    },

    addItem: async (variantId, quantity) => {
        const response = await api.post('/cart/items', { variantId, quantity });
        return response.data;
    },

    updateQuantity: async (variantId, quantity) => {
        const response = await api.put(`/cart/items/${variantId}`, { quantity });
        return response.data;
    },

    removeItem: async (variantId) => {
        const response = await api.delete(`/cart/items/${variantId}`);
        return response.data;
    },

    clearCart: async () => {
        const response = await api.delete('/cart');
        return response.data;
    }
};

export default cartService;
