const brandService = require('../services/brand.service');
const { successResponse, errorResponse } = require('../utils/response.util');

/**
 * Get all brands
 * GET /api/v1/brands
 */
const getAllBrands = async (req, res) => {
    try {
        const brands = await brandService.getAllBrands();
        return successResponse(res, brands, 'Brands retrieved successfully');
    } catch (error) {
        console.error('Error in getAllBrands:', error);
        return errorResponse(res, error.message, 500);
    }
};

/**
 * Get brand by ID
 * GET /api/v1/brands/:id
 */
const getBrandById = async (req, res) => {
    try {
        const { id } = req.params;
        const brand = await brandService.getBrandById(id);

        if (!brand) {
            return errorResponse(res, 'Brand not found', 404);
        }

        return successResponse(res, brand, 'Brand retrieved successfully');
    } catch (error) {
        console.error('Error in getBrandById:', error);
        return errorResponse(res, error.message, 500);
    }
};

module.exports = {
    getAllBrands,
    getBrandById
};
