const express = require('express');
const router = express.Router();
const brandController = require('../controllers/brand.controller');

/**
 * @route   GET /api/v1/brands
 * @desc    Get all brands
 * @access  Public
 */
router.get('/', brandController.getAllBrands);

/**
 * @route   GET /api/v1/brands/:id
 * @desc    Get brand by ID
 * @access  Public
 */
router.get('/:id', brandController.getBrandById);

module.exports = router;
