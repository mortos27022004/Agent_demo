const db = require('../../config/database');

/**
 * Get all brands
 * @returns {Promise<Array>} List of brands
 */
const getAllBrands = async () => {
    try {
        const query = 'SELECT id, name, slug FROM brands ORDER BY name ASC';
        const result = await db.query(query);
        return result.rows;
    } catch (error) {
        throw error;
    }
};

/**
 * Get brand by ID
 * @param {string} id - Brand UUID
 * @returns {Promise<Object>} Brand object
 */
const getBrandById = async (id) => {
    try {
        const query = 'SELECT * FROM brands WHERE id = $1';
        const result = await db.query(query, [id]);
        return result.rows[0];
    } catch (error) {
        throw error;
    }
};

module.exports = {
    getAllBrands,
    getBrandById
};
