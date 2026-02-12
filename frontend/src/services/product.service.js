import api from './api';

const productService = {
    /**
     * Get all products with optional filters
     * @param {Object} params - Query parameters (page, limit, search, category_id, brand_id, published)
     * @returns {Promise<Object>} Products with pagination info
     */
    getAllProducts: async (params = {}) => {
        try {
            const response = await api.get('/products', { params });
            return response.data.data;
        } catch (error) {
            throw error;
        }
    },

    /**
     * Get product by ID
     * @param {string} id - Product UUID
     * @returns {Promise<Object>} Product details
     */
    getProductById: async (id) => {
        try {
            const response = await api.get(`/products/${id}`);
            return response.data.data;
        } catch (error) {
            throw error;
        }
    },

    /**
     * Create new product with variants
     * @param {Object} productData - Product data including variants and images
     * @returns {Promise<Object>} Created product
     */
    createProduct: async (productData) => {
        try {
            const response = await api.post('/products', productData);
            return response.data.data;
        } catch (error) {
            throw error;
        }
    },

    /**
     * Update existing product
     * @param {string} id - Product UUID
     * @param {Object} productData - Updated product data
     * @returns {Promise<Object>} Updated product
     */
    updateProduct: async (id, productData) => {
        try {
            const response = await api.put(`/products/${id}`, productData);
            return response.data.data;
        } catch (error) {
            throw error;
        }
    },

    /**
     * Upload an image file to the backend
     * @param {File} file - The file object to upload
     * @returns {Promise<Object>} Uploaded image info (url, filename)
     */
    uploadImage: async (file) => {
        try {
            const formData = new FormData();
            formData.append('image', file);
            const response = await api.post('/upload/single', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            return response.data.data;
        } catch (error) {
            throw error;
        }
    }
};

export default productService;
