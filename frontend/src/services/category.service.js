import api from './api';

const categoryService = {
    /**
     * Get all categories
     * @returns {Promise<Array>} List of categories
     */
    getAllCategories: async () => {
        try {
            const response = await api.get('/categories');
            return response.data.data;
        } catch (error) {
            throw error;
        }
    },

    /**
     * Create new category
     * @param {Object} categoryData - Category data
     * @returns {Promise<Object>} Created category
     */
    createCategory: async (categoryData) => {
        try {
            const response = await api.post('/categories', categoryData);
            return response.data.data;
        } catch (error) {
            throw error;
        }
    },

    /**
     * Update category
     * @param {string} id - Category UUID
     * @param {Object} categoryData - Category data
     * @returns {Promise<Object>} Updated category
     */
    updateCategory: async (id, categoryData) => {
        try {
            const response = await api.put(`/categories/${id}`, categoryData);
            return response.data.data;
        } catch (error) {
            throw error;
        }
    },

    /**
     * Delete category
     * @param {string} id - Category UUID
     * @returns {Promise<boolean>} Success status
     */
    deleteCategory: async (id) => {
        try {
            const response = await api.delete(`/categories/${id}`);
            return response.data.data;
        } catch (error) {
            throw error;
        }
    }
};

export default categoryService;
