const path = require('path');

const uploadImage = (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({
                status: 'error',
                message: 'Vui lòng chọn ảnh để tải lên'
            });
        }

        const baseUrl = process.env.BASE_URL || '';
        const imageUrl = `${baseUrl}/uploads/${req.file.filename}`;

        res.status(200).json({
            status: 'success',
            data: {
                url: imageUrl,
                filename: req.file.filename,
                originalName: req.file.originalname,
                size: req.file.size
            }
        });
    } catch (error) {
        console.error('Error in uploadImage:', error);
        res.status(500).json({
            status: 'error',
            message: error.message
        });
    }
};

const uploadImages = (req, res) => {
    try {
        if (!req.files || req.files.length === 0) {
            return res.status(400).json({
                status: 'error',
                message: 'Vui lòng chọn ảnh để tải lên'
            });
        }

        const baseUrl = process.env.BASE_URL || '';
        const imageUrls = req.files.map(file => ({
            url: `${baseUrl}/uploads/${file.filename}`,
            filename: file.filename,
            originalName: file.originalname,
            size: file.size
        }));

        res.status(200).json({
            status: 'success',
            data: imageUrls
        });
    } catch (error) {
        console.error('Error in uploadImages:', error);
        res.status(500).json({
            status: 'error',
            message: error.message
        });
    }
};

module.exports = {
    uploadImage,
    uploadImages
};
