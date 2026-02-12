const db = require('../../config/database');

/**
 * Get or create an open cart for a user
 * @param {string} userId - User UUID
 * @returns {Promise<Object>} Cart object
 */
const getOrCreateCart = async (userId) => {
    try {
        console.log('getOrCreateCart for userId:', userId);
        // Try to find an open cart
        const findQuery = 'SELECT * FROM carts WHERE user_id = $1 AND status = \'open\' ORDER BY created_at DESC LIMIT 1';
        const findResult = await db.query(findQuery, [userId]);

        if (findResult.rows.length > 0) {
            console.log('Found existing cart:', findResult.rows[0].id);
            return findResult.rows[0];
        }

        // Create new cart if none found
        const createQuery = 'INSERT INTO carts (user_id, status) VALUES ($1, \'open\') RETURNING *';
        const createResult = await db.query(createQuery, [userId]);
        console.log('Created new cart:', createResult.rows[0].id);
        return createResult.rows[0];
    } catch (error) {
        console.error('Error in getOrCreateCart:', error);
        throw error;
    }
};

/**
 * Get all items in a cart
 * @param {string} cartId - Cart UUID
 * @returns {Promise<Array>} List of items with variant and product details
 */
const getCartItems = async (cartId) => {
    try {
        const query = `
            SELECT 
                ci.variant_id,
                ci.quantity,
                pv.sku,
                pv.variant_name,
                pv.price,
                pv.compare_at,
                pv.attributes as variant_attributes,
                p.id as product_id,
                p.name as product_name,
                p.slug as product_slug,
                (
                    SELECT pai.image_urls[1]
                    FROM product_attribute_images pai
                    WHERE pai.product_id = p.id 
                    AND (pv.attributes @> pai.attribute_combo OR pai.attribute_combo = '{}'::jsonb OR pai.attribute_combo = '[]'::jsonb)
                    ORDER BY CASE WHEN pv.attributes @> pai.attribute_combo THEN 0 ELSE 1 END, pai.created_at ASC
                    LIMIT 1
                ) as image_url
            FROM cart_items ci
            JOIN product_variants pv ON ci.variant_id = pv.id
            JOIN products p ON pv.product_id = p.id
            WHERE ci.cart_id = $1
        `;
        const result = await db.query(query, [cartId]);

        const baseUrl = process.env.BASE_URL || '';
        return result.rows.map(item => ({
            ...item,
            image_url: (item.image_url && !item.image_url.startsWith('http'))
                ? `${baseUrl}${item.image_url}`
                : item.image_url
        }));
    } catch (error) {
        console.error('Error in getCartItems:', error);
        throw error;
    }
};

/**
 * Add an item to the cart
 * @param {string} cartId - Cart UUID
 * @param {string} variantId - Variant UUID
 * @param {number} quantity - Quantity to add
 */
const addItemToCart = async (cartId, variantId, quantity) => {
    try {
        console.log(`Adding item to cart: cartId=${cartId}, variantId=${variantId}, quantity=${quantity}`);
        const query = `
            INSERT INTO cart_items (cart_id, variant_id, quantity)
            VALUES ($1, $2, $3)
            ON CONFLICT (cart_id, variant_id)
            DO UPDATE SET 
                quantity = cart_items.quantity + $3
            RETURNING *
        `;
        // Note: The schema doesn't have updated_at on cart_items, but let's update the cart last_updated
        const result = await db.query(query, [cartId, variantId, quantity]);
        console.log('Item added/updated in database:', result.rows[0]);

        await db.query('UPDATE carts SET updated_at = NOW() WHERE id = $1', [cartId]);

        return result.rows[0];
    } catch (error) {
        console.error('Error in addItemToCart:', error);
        throw error;
    }
};

/**
 * Update item quantity in cart
 * @param {string} cartId - Cart UUID
 * @param {string} variantId - Variant UUID
 * @param {number} quantity - New quantity
 */
const updateItemQuantity = async (cartId, variantId, quantity) => {
    try {
        const query = `
            UPDATE cart_items 
            SET quantity = $3
            WHERE cart_id = $1 AND variant_id = $2
            RETURNING *
        `;
        const result = await db.query(query, [cartId, variantId, quantity]);

        await db.query('UPDATE carts SET updated_at = NOW() WHERE id = $1', [cartId]);

        return result.rows[0];
    } catch (error) {
        throw error;
    }
};

/**
 * Remove item from cart
 * @param {string} cartId - Cart UUID
 * @param {string} variantId - Variant UUID
 */
const removeItemFromCart = async (cartId, variantId) => {
    try {
        await db.query('DELETE FROM cart_items WHERE cart_id = $1 AND variant_id = $2', [cartId, variantId]);
        await db.query('UPDATE carts SET updated_at = NOW() WHERE id = $1', [cartId]);
        return true;
    } catch (error) {
        throw error;
    }
};

/**
 * Clear all items from a cart
 * @param {string} cartId - Cart UUID
 */
const clearCart = async (cartId) => {
    try {
        await db.query('DELETE FROM cart_items WHERE cart_id = $1', [cartId]);
        await db.query('UPDATE carts SET updated_at = NOW() WHERE id = $1', [cartId]);
        return true;
    } catch (error) {
        throw error;
    }
};

module.exports = {
    getOrCreateCart,
    getCartItems,
    addItemToCart,
    updateItemQuantity,
    removeItemFromCart,
    clearCart
};
