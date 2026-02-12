const orderService = require('../services/order.service');
const { successResponse, errorResponse } = require('../utils/response.util');

const createOrder = async (req, res) => {
    try {
        const userId = req.user.id;
        const orderData = req.body;

        if (!orderData.address || !orderData.payment_method) {
            return errorResponse(res, 'Address and payment method are required', 400);
        }

        const order = await orderService.createOrder(userId, orderData);
        return successResponse(res, order, 'Order placed successfully', 201);
    } catch (error) {
        console.error('Create Order Error:', error);
        return errorResponse(res, error.message);
    }
};

const getMyOrders = async (req, res) => {
    try {
        const userId = req.user.id;
        const orders = await orderService.getUserOrders(userId);
        return successResponse(res, orders, 'Orders retrieved successfully');
    } catch (error) {
        return errorResponse(res, error.message);
    }
};

const getOrderDetail = async (req, res) => {
    try {
        const userId = req.user.id;
        const { id } = req.params;
        const order = await orderService.getOrderById(id, userId);

        if (!order) {
            return errorResponse(res, 'Order not found', 404);
        }

        return successResponse(res, order, 'Order details retrieved');
    } catch (error) {
        return errorResponse(res, error.message);
    }
};

module.exports = {
    createOrder,
    getMyOrders,
    getOrderDetail
};
