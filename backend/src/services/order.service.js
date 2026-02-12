const db = require('../../config/database');

/**
 * Create a new order from a user's cart
 * @param {string} userId - User UUID
 * @param {Object} orderData - Order details (address, payment_method, notes)
 * @returns {Promise<Object>} Created order
 */
const createOrder = async (userId, orderData) => {
    const client = await db.connect();
    try {
        await client.query('BEGIN');

        const { address, payment_method, notes } = orderData;

        // 1. Get user's open cart and items
        const cartQuery = 'SELECT id FROM carts WHERE user_id = $1 AND status = \'open\' ORDER BY created_at DESC LIMIT 1';
        const cartResult = await client.query(cartQuery, [userId]);

        if (cartResult.rows.length === 0) {
            throw new Error('No open cart found');
        }

        const cartId = cartResult.rows[0].id;
        const itemsQuery = `
            SELECT ci.*, pv.price, pv.sku, p.name as product_name, pv.variant_name
            FROM cart_items ci
            JOIN product_variants pv ON ci.variant_id = pv.id
            JOIN products p ON pv.product_id = p.id
            WHERE ci.cart_id = $1
        `;
        const itemsResult = await client.query(itemsQuery, [cartId]);

        if (itemsResult.rows.length === 0) {
            throw new Error('Cart is empty');
        }

        // 2. Calculate totals
        const subtotal = itemsResult.rows.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        const shippingFee = 30000; // Flat fee for now
        const total = subtotal + shippingFee;
        const orderCode = `ORD-${Date.now()}-${Math.floor(Math.random() * 1000)}`;

        // 3. Create order
        const insertOrderQuery = `
            INSERT INTO orders (
                user_id, order_code, status, currency, 
                subtotal, shipping_fee, total, 
                shipping_address, customer_notes
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING *
        `;
        const orderResult = await client.query(insertOrderQuery, [
            userId, orderCode, 'pending', 'VND',
            subtotal, shippingFee, total,
            JSON.stringify(address), notes
        ]);
        const order = orderResult.rows[0];

        // 4. Create order items
        for (const item of itemsResult.rows) {
            const insertOrderItemQuery = `
                INSERT INTO order_items (
                    order_id, variant_id, sku, name, 
                    unit_price, quantity, line_total
                ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            `;
            await client.query(insertOrderItemQuery, [
                order.id,
                item.variant_id,
                item.sku,
                `${item.product_name}${item.variant_name ? ' - ' + item.variant_name : ''}`,
                item.price,
                item.quantity,
                item.price * item.quantity
            ]);

            // 5. Update inventory
            const updateInventoryQuery = `
                UPDATE inventory 
                SET on_hand = on_hand - $1 
                WHERE variant_id = $2
            `;
            await client.query(updateInventoryQuery, [item.quantity, item.variant_id]);
        }

        // 6. Record payment placeholder
        const insertPaymentQuery = `
            INSERT INTO payments (order_id, provider, amount, status)
            VALUES ($1, $2, $3, $4)
        `;
        await client.query(insertPaymentQuery, [
            order.id,
            payment_method,
            total,
            payment_method === 'cod' ? 'pending' : 'initiated'
        ]);

        // 7. Clear cart items and close cart
        await client.query('DELETE FROM cart_items WHERE cart_id = $1', [cartId]);
        await client.query('UPDATE carts SET status = \'converted\', updated_at = NOW() WHERE id = $1', [cartId]);

        // 8. Add order history
        await client.query('INSERT INTO order_status_history (order_id, status, comment) VALUES ($1, $2, $3)', [
            order.id, 'pending', 'Order placed successfully'
        ]);

        await client.query('COMMIT');
        return order;
    } catch (error) {
        await client.query('ROLLBACK');
        throw error;
    } finally {
        client.release();
    }
};

/**
 * Get all orders for a user
 */
const getUserOrders = async (userId) => {
    const query = `
        SELECT o.*, 
            (SELECT json_agg(oi) FROM order_items oi WHERE oi.order_id = o.id) as items
        FROM orders o
        WHERE o.user_id = $1
        ORDER BY o.created_at DESC
    `;
    const result = await db.query(query, [userId]);
    return result.rows;
};

/**
 * Get order detail by ID
 */
const getOrderById = async (orderId, userId) => {
    const query = `
        SELECT o.*, 
            json_agg(oi) as items,
            p.provider as payment_provider,
            p.status as payment_status
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        LEFT JOIN payments p ON o.id = p.order_id
        WHERE o.id = $1 AND o.user_id = $2
        GROUP BY o.id, p.id
    `;
    const result = await db.query(query, [orderId, userId]);
    return result.rows[0];
};

module.exports = {
    createOrder,
    getUserOrders,
    getOrderById
};
