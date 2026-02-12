const express = require('express');
const router = express.Router();
const productController = require('../controllers/product.controller');

/**
 * @route   GET /api/v1/products
 * @desc    Get all products with pagination and filters
 * @access  Public
 */
router.get('/', productController.getAllProducts);

/**
 * @route   GET /api/v1/products/:id
 * @desc    Get product by ID
 * @access  Public
 */
router.get('/:id', productController.getProductById);

/**
 * @route   POST /api/v1/products
 * @desc    Get product by ID
 * @access  Public
 */
router.post('/', productController.createProduct);

/**
 * @route   PUT /api/v1/products/:id
 * @desc    Update existing product
 * @access  Admin (TODO: add auth middleware)
 */
router.put('/:id', productController.updateProduct);

module.exports = router;
