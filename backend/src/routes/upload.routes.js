const express = require('express');
const router = express.Router();
const uploadController = require('../controllers/upload.controller');
const upload = require('../utils/upload');

// Single image upload
router.post('/single', upload.single('image'), uploadController.uploadImage);

// Multiple images upload
router.post('/multiple', upload.array('images', 10), uploadController.uploadImages);

module.exports = router;
