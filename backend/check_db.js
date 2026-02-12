require('dotenv').config();
const db = require('./config/database');
const fs = require('fs');

async function checkProduct(productId) {
    const results = {};
    try {
        const productRes = await db.query('SELECT * FROM products WHERE id = $1', [productId]);
        results.product = productRes.rows[0];

        const variantRes = await db.query('SELECT * FROM product_variants WHERE product_id = $1', [productId]);
        results.variants = variantRes.rows;
        results.variantCount = variantRes.rowCount;

        const imgRes = await db.query('SELECT * FROM product_attribute_images WHERE product_id = $1', [productId]);
        results.attributeImages = imgRes.rows;
        results.attributeImageCount = imgRes.rowCount;

        fs.writeFileSync('db_results.json', JSON.stringify(results, null, 2));
        console.log('Results written to db_results.json');

    } catch (err) {
        console.error('Error:', err);
    } finally {
        process.exit();
    }
}

const productId = process.argv[2] || '0a255ed8-734b-420c-ae72-08610008de39';
checkProduct(productId);
