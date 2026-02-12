require('dotenv').config();
const productService = require('./src/services/product.service');
const db = require('./config/database');

async function test() {
    try {
        const productId = '0d5a3f4a-7b50-4c66-8aab-1f2f8e0c2a11';
        const product = await productService.getProductById(productId);
        console.log('PRODUCT_JSON_START');
        console.log(JSON.stringify(product, null, 2));
        console.log('PRODUCT_JSON_END');
    } catch (error) {
        console.error('Test failed:', error);
    } finally {
        // Close DB connection if needed, though pg pool might just hang
        process.exit();
    }
}

test();
