const cartService = require('../services/cart.service');
const { successResponse, errorResponse } = require('../utils/response.util');

const getCart = async (req, res) => {
    try {
        const userId = req.user.id;
        const cart = await cartService.getOrCreateCart(userId);
        const items = await cartService.getCartItems(cart.id);

        return successResponse(res, {
            ...cart,
            items
        }, 'Cart retrieved successfully');
    } catch (error) {
        return errorResponse(res, error.message);
    }
};

const addItem = async (req, res) => {
    try {
        const userId = req.user.id;
        const { variantId, quantity } = req.body;

        if (!variantId || !quantity) {
            return errorResponse(res, 'Variant ID and quantity are required', 400);
        }

        const cart = await cartService.getOrCreateCart(userId);
        const item = await cartService.addItemToCart(cart.id, variantId, parseInt(quantity));

        return successResponse(res, item, 'Item added to cart successfully');
    } catch (error) {
        return errorResponse(res, error.message);
    }
};

const updateItem = async (req, res) => {
    try {
        const userId = req.user.id;
        const { variantId } = req.params;
        const { quantity } = req.body;

        if (quantity === undefined) {
            return errorResponse(res, 'Quantity is required', 400);
        }

        const cart = await cartService.getOrCreateCart(userId);

        if (parseInt(quantity) <= 0) {
            await cartService.removeItemFromCart(cart.id, variantId);
            return successResponse(res, null, 'Item removed from cart');
        }

        const item = await cartService.updateItemQuantity(cart.id, variantId, parseInt(quantity));
        return successResponse(res, item, 'Item quantity updated');
    } catch (error) {
        return errorResponse(res, error.message);
    }
};

const removeItem = async (req, res) => {
    try {
        const userId = req.user.id;
        const { variantId } = req.params;

        const cart = await cartService.getOrCreateCart(userId);
        await cartService.removeItemFromCart(cart.id, variantId);

        return successResponse(res, null, 'Item removed from cart');
    } catch (error) {
        return errorResponse(res, error.message);
    }
};

const clearCart = async (req, res) => {
    try {
        const userId = req.user.id;
        const cart = await cartService.getOrCreateCart(userId);
        await cartService.clearCart(cart.id);

        return successResponse(res, null, 'Cart cleared');
    } catch (error) {
        return errorResponse(res, error.message);
    }
};

module.exports = {
    getCart,
    addItem,
    updateItem,
    removeItem,
    clearCart
};
