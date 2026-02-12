const express = require('express');
const router = express.Router();
const categoryController = require('../controllers/category.controller');
// const { authenticate, authorize } = require('../middleware/auth.middleware'); // Logic for admin auth

/**
 * @route   GET /api/v1/categories
 * @desc    Get all categories
 * @access  Public
 */
router.get('/', categoryController.getAllCategories);

/**
 * @route   POST /api/v1/categories
 * @desc    Create new category
 * @access  Admin Only
 */
router.post('/', categoryController.createCategory);

/**
 * @route   PUT /api/v1/categories/:id
 * @desc    Update category
 * @access  Admin Only
 */
router.put('/:id', categoryController.updateCategory);

/**
 * @route   DELETE /api/v1/categories/:id
 * @desc    Delete category
 * @access  Admin Only
 */
router.delete('/:id', categoryController.deleteCategory);

module.exports = router;
