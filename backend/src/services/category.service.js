const db = require('../../config/database');

/**
 * Get all categories
 * @returns {Promise<Array>} List of categories
 */
const getAllCategories = async () => {
    try {
        const query = `
            SELECT 
                id, 
                parent_id, 
                name, 
                slug,
                icon,
                status,
                attributes,
                (SELECT COUNT(*) FROM products WHERE category_id = categories.id) as product_count
            FROM categories
            ORDER BY name ASC
        `;
        const result = await db.query(query);
        return result.rows;
    } catch (error) {
        throw error;
    }
};

/**
 * Get category by ID
 * @param {string} id - Category UUID
 * @returns {Promise<Object>} Category object
 */
const getCategoryById = async (id) => {
    try {
        const query = 'SELECT * FROM categories WHERE id = $1';
        const result = await db.query(query, [id]);
        return result.rows[0];
    } catch (error) {
        throw error;
    }
};

/**
 * Create new category
 * @param {Object} categoryData - Category data
 * @returns {Promise<Object>} Created category
 */
const createCategory = async (categoryData) => {
    try {
        const { name, slug, parent_id, icon } = categoryData;
        const query = `
            INSERT INTO categories (name, slug, parent_id, icon, status, attributes)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING *
        `;
        const result = await db.query(query, [
            name,
            slug,
            parent_id || null,
            icon || 'info-circle',
            status || 'active',
            JSON.stringify(attributes || [])
        ]);
        return result.rows[0];
    } catch (error) {
        throw error;
    }
};

/**
 * Update category
 * @param {string} id - Category UUID
 * @param {Object} categoryData - Category data
 * @returns {Promise<Object>} Updated category
 */
const updateCategory = async (id, categoryData) => {
    try {
        const { name, slug, parent_id, icon, status, attributes } = categoryData;
        const query = `
            UPDATE categories
            SET name = $1, slug = $2, parent_id = $3, icon = $4, status = $5, attributes = $6
            WHERE id = $7
            RETURNING *
        `;
        const result = await db.query(query, [
            name,
            slug,
            parent_id || null,
            icon || 'info-circle',
            status || 'active',
            JSON.stringify(attributes || []),
            id
        ]);
        return result.rows[0];
    } catch (error) {
        throw error;
    }
};

/**
 * Delete category
 * @param {string} id - Category UUID
 * @returns {Promise<boolean>} Success status
 */
const deleteCategory = async (id) => {
    try {
        await db.query('DELETE FROM categories WHERE id = $1', [id]);
        return true;
    } catch (error) {
        throw error;
    }
};

module.exports = {
    getAllCategories,
    getCategoryById,
    createCategory,
    updateCategory,
    deleteCategory
};
