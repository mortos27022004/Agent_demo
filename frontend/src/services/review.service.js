import api from './api';

const reviewService = {
    getProductReviews: async (productId) => {
        const response = await api.get(`/reviews/product/${productId}`);
        return response.data;
    },
    addReview: async (reviewData) => {
        const response = await api.post('/reviews', reviewData);
        return response.data;
    }
};

export default reviewService;
