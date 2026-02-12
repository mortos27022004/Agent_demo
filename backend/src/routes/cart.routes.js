const express = require('express');
const router = express.Router();
const cartController = require('../controllers/cart.controller');
const { protect } = require('../middleware/auth.middleware');

// All cart routes require authentication
router.use(protect);

router.get('/', cartController.getCart);
router.post('/items', cartController.addItem);
router.put('/items/:variantId', cartController.updateItem);
router.delete('/items/:variantId', cartController.removeItem);
router.delete('/', cartController.clearCart);

module.exports = router;
