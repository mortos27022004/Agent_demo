import api from './api';

const brandService = {
    /**
     * Get all brands
     * @returns {Promise<Array>} List of brands
     */
    getAllBrands: async () => {
        try {
            const response = await api.get('/brands');
            return response.data.data;
        } catch (error) {
            throw error;
        }
    }
};

export default brandService;
