const reviewService = require('../services/review.service');
const { successResponse, errorResponse } = require('../utils/response.util');

const addReview = async (req, res) => {
    try {
        const userId = req.user.id;
        const review = await reviewService.addReview(userId, req.body);
        return successResponse(res, review, 'Review added successfully', 201);
    } catch (error) {
        return errorResponse(res, error.message);
    }
};

const getProductReviews = async (req, res) => {
    try {
        const { productId } = req.params;
        const reviews = await reviewService.getProductReviews(productId);
        return successResponse(res, reviews, 'Reviews retrieved successfully');
    } catch (error) {
        return errorResponse(res, error.message);
    }
};

module.exports = {
    addReview,
    getProductReviews
};
