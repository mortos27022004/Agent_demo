const db = require('../../config/database');

/**
 * Add a review for a product
 */
const addReview = async (userId, reviewData) => {
    const { productId, rating, comment } = reviewData;

    // Check if user has purchased the product
    const purchaseQuery = `
        SELECT 1 FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN product_variants pv ON oi.variant_id = pv.id
        WHERE o.user_id = $1 AND pv.product_id = $2 AND o.status = 'completed'
        LIMIT 1
    `;
    const purchaseResult = await db.query(purchaseQuery, [userId, productId]);
    const isVerifiedPurchase = purchaseResult.rows.length > 0;

    const query = `
        INSERT INTO reviews (user_id, product_id, rating, comment, is_verified_purchase)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING *
    `;
    const result = await db.query(query, [userId, productId, rating, comment, isVerifiedPurchase]);
    return result.rows[0];
};

/**
 * Get reviews for a product
 */
const getProductReviews = async (productId) => {
    const query = `
        SELECT r.*, u.full_name as user_name
        FROM reviews r
        JOIN users u ON r.user_id = u.id
        WHERE r.product_id = $1 AND r.status = 'approved'
        ORDER BY r.created_at DESC
    `;
    const result = await db.query(query, [productId]);
    return result.rows;
};

module.exports = {
    addReview,
    getProductReviews
};
