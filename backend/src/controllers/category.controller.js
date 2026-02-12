const categoryService = require('../services/category.service');
const { successResponse, errorResponse } = require('../utils/response.util');

/**
 * Get all categories
 * GET /api/v1/categories
 */
const getAllCategories = async (req, res) => {
    try {
        const categories = await categoryService.getAllCategories();
        return successResponse(res, categories, 'Categories retrieved successfully');
    } catch (error) {
        console.error('Error in getAllCategories:', error);
        return errorResponse(res, error.message, 500);
    }
};

/**
 * Create new category
 * POST /api/v1/categories
 */
const createCategory = async (req, res) => {
    try {
        const category = await categoryService.createCategory(req.body);
        return successResponse(res, category, 'Category created successfully', 201);
    } catch (error) {
        console.error('Error in createCategory:', error);
        return errorResponse(res, error.message, 500);
    }
};

/**
 * Update category
 * PUT /api/v1/categories/:id
 */
const updateCategory = async (req, res) => {
    try {
        const { id } = req.params;
        const category = await categoryService.updateCategory(id, req.body);

        if (!category) {
            return errorResponse(res, 'Category not found', 404);
        }

        return successResponse(res, category, 'Category updated successfully');
    } catch (error) {
        console.error('Error in updateCategory:', error);
        return errorResponse(res, error.message, 500);
    }
};

/**
 * Delete category
 * DELETE /api/v1/categories/:id
 */
const deleteCategory = async (req, res) => {
    try {
        const { id } = req.params;
        await categoryService.deleteCategory(id);
        return successResponse(res, null, 'Category deleted successfully');
    } catch (error) {
        console.error('Error in deleteCategory:', error);
        return errorResponse(res, error.message, 500);
    }
};

module.exports = {
    getAllCategories,
    createCategory,
    updateCategory,
    deleteCategory
};
