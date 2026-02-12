const db = require('../../config/database');

const stripBaseUrlFromImages = (attribute_images) => {
  if (!attribute_images || !Array.isArray(attribute_images)) return [];
  const baseUrl = process.env.BASE_URL || '';

  return attribute_images.map(ai => ({
    ...ai,
    image_urls: ai.image_urls.map(url => {
      if (url && url.startsWith(baseUrl) && baseUrl !== '') {
        return url.replace(baseUrl, '');
      }
      return url;
    })
  }));
};

/**
 * Get all products with variants and basic information
 * @param {Object} filters - Optional filters (category, brand, search, etc.)
 * @returns {Promise<Array>} List of products
 */
const getAllProducts = async (filters = {}) => {
  try {
    let query = `
      WITH product_images AS (
        SELECT 
          product_id,
          image_urls[1] as first_image
        FROM product_attribute_images
        WHERE attribute_combo = '{}'::jsonb OR attribute_combo = '[]'::jsonb
        ORDER BY created_at ASC
      )
      SELECT 
        p.id,
        p.name,
        p.sku,
        p.slug,
        p.description,
        p.is_published,
        p.created_at,
        c.name as category_name,
        b.name as brand_name,
        (SELECT first_image FROM product_images WHERE product_id = p.id LIMIT 1) as main_image,
        COALESCE(
          json_agg(
            jsonb_build_object(
              'id', pv.id,
              'sku', pv.sku,
              'variant_name', pv.variant_name,
              'price', pv.price,
              'compare_at', pv.compare_at,
              'status', pv.status,
              'attributes', pv.attributes,
              'image', (
                SELECT pai.image_urls[1]
                FROM product_attribute_images pai
                WHERE pai.product_id = p.id 
                AND (pv.attributes @> pai.attribute_combo OR pai.attribute_combo = '{}'::jsonb OR pai.attribute_combo = '[]'::jsonb)
                ORDER BY CASE WHEN pv.attributes @> pai.attribute_combo THEN 0 ELSE 1 END, pai.created_at ASC
                LIMIT 1
              )
            )
          ) FILTER (WHERE pv.id IS NOT NULL),
          '[]'
        ) as variants
      FROM products p
      LEFT JOIN categories c ON p.category_id = c.id
      LEFT JOIN brands b ON p.brand_id = b.id
      LEFT JOIN product_variants pv ON p.id = pv.product_id
    `;

    const conditions = [];
    const params = [];
    let paramIndex = 1;

    // Filter by published status
    if (filters.published !== undefined) {
      conditions.push(`p.is_published = $${paramIndex}`);
      params.push(filters.published);
      paramIndex++;
    }

    // Filter by category
    if (filters.category_id) {
      conditions.push(`p.category_id = $${paramIndex}`);
      params.push(filters.category_id);
      paramIndex++;
    }

    // Filter by brand
    if (filters.brand_id) {
      conditions.push(`p.brand_id = $${paramIndex}`);
      params.push(filters.brand_id);
      paramIndex++;
    }

    // Search by name (keyword)
    if (filters.search) {
      conditions.push(`(p.name ILIKE $${paramIndex} OR p.description ILIKE $${paramIndex})`);
      params.push(`%${filters.search}%`);
      paramIndex++;
    }

    // Filter by min price
    if (filters.minPrice) {
      conditions.push(`pv.price >= $${paramIndex}`);
      params.push(filters.minPrice);
      paramIndex++;
    }

    // Filter by max price
    if (filters.maxPrice) {
      conditions.push(`pv.price <= $${paramIndex}`);
      params.push(filters.maxPrice);
      paramIndex++;
    }

    // Filter by attributes (dynamic)
    if (filters.attributes && typeof filters.attributes === 'object') {
      Object.entries(filters.attributes).forEach(([key, value]) => {
        if (value) {
          conditions.push(`pv.attributes->>$${paramIndex} = $${paramIndex + 1}`);
          params.push(key, value);
          paramIndex += 2;
        }
      });
    }

    if (conditions.length > 0) {
      query += ' WHERE ' + conditions.join(' AND ');
    }

    query += ' GROUP BY p.id, c.name, b.name ORDER BY p.created_at DESC';

    // Pagination
    const limit = filters.limit || 20;
    const offset = filters.offset || 0;

    query += ` LIMIT $${paramIndex} OFFSET $${paramIndex + 1}`;
    params.push(limit, offset);

    const result = await db.query(query, params);
    const baseUrl = process.env.BASE_URL || '';

    // Process images to add base URL
    const products = result.rows.map(product => {
      // Add base URL to main_image
      if (product.main_image && !product.main_image.startsWith('http')) {
        product.main_image = `${baseUrl}${product.main_image}`;
      }

      // Add base URL to variant images
      if (product.variants) {
        product.variants = product.variants.map(v => ({
          ...v,
          image: (v.image && !v.image.startsWith('http')) ? `${baseUrl}${v.image}` : v.image
        }));
      }

      return product;
    });

    return products;
  } catch (error) {
    throw error;
  }
};

/**
 * Get product by ID with full details
 * @param {string} productId - Product UUID
 * @returns {Promise<Object>} Product details
 */
const getProductById = async (productId) => {
  try {
    const query = `
      SELECT 
        p.id,
        p.name,
        p.sku,
        p.slug,
        p.description,
        p.specs,
        p.is_published,
        p.created_at,
        p.updated_at,
        c.id as category_id,
        c.name as category_name,
        b.id as brand_id,
        b.name as brand_name,
        (
          SELECT COALESCE(
            json_agg(
              jsonb_build_object(
                'id', pv.id,
                'sku', pv.sku,
                'variant_name', pv.variant_name,
                'price', pv.price,
                'compare_at', pv.compare_at,
                'cost', pv.cost,
                'status', pv.status,
                'attributes', pv.attributes,
                'image', (
                  SELECT pai.image_urls[1]
                  FROM product_attribute_images pai
                  WHERE pai.product_id = p.id 
                  AND (pv.attributes @> pai.attribute_combo OR pai.attribute_combo = '{}'::jsonb OR pai.attribute_combo = '[]'::jsonb)
                  ORDER BY CASE WHEN pv.attributes @> pai.attribute_combo THEN 0 ELSE 1 END, pai.created_at ASC
                  LIMIT 1
                )
              )
            ),
            '[]'
          )
          FROM product_variants pv
          WHERE pv.product_id = p.id
        ) as variants,
        (
          SELECT first_image FROM (
            SELECT image_urls[1] as first_image 
            FROM product_attribute_images 
            WHERE product_id = p.id 
            AND (attribute_combo = '{}'::jsonb OR attribute_combo = '[]'::jsonb)
            ORDER BY created_at ASC 
            LIMIT 1
          ) tmp
        ) as main_image,
        (
          SELECT COALESCE(
            json_agg(
              jsonb_build_object(
                'id', pai.id,
                'attribute_combo', pai.attribute_combo,
                'image_urls', pai.image_urls
              )
            ),
            '[]'
          )
          FROM product_attribute_images pai
          WHERE pai.product_id = p.id
        ) as attribute_images
      FROM products p
      LEFT JOIN categories c ON p.category_id = c.id
      LEFT JOIN brands b ON p.brand_id = b.id
      WHERE p.id = $1
    `;

    const result = await db.query(query, [productId]);
    const product = result.rows[0];

    if (product) {
      const baseUrl = process.env.BASE_URL || '';

      // Process main_image
      if (product.main_image && !product.main_image.startsWith('http')) {
        product.main_image = `${baseUrl}${product.main_image}`;
      }

      // Process attribute_images (existing)
      if (product.attribute_images) {
        product.attribute_images = product.attribute_images.map(ai => ({
          ...ai,
          image_urls: ai.image_urls.map(url =>
            (url && !url.startsWith('http')) ? `${baseUrl}${url}` : url
          )
        }));
      }

      // Process variants images
      if (product.variants) {
        product.variants = product.variants.map(v => ({
          ...v,
          image: (v.image && !v.image.startsWith('http')) ? `${baseUrl}${v.image}` : v.image
        }));
      }
    }

    return product || null;
  } catch (error) {
    throw error;
  }
};

/**
 * Get product count for pagination
 * @param {Object} filters - Optional filters
 * @returns {Promise<number>} Total count
 */
const getProductCount = async (filters = {}) => {
  try {
    let query = 'SELECT COUNT(*) FROM products p';
    const conditions = [];
    const params = [];
    let paramIndex = 1;

    if (filters.published !== undefined) {
      conditions.push(`p.is_published = $${paramIndex}`);
      params.push(filters.published);
      paramIndex++;
    }

    if (filters.category_id) {
      conditions.push(`p.category_id = $${paramIndex}`);
      params.push(filters.category_id);
      paramIndex++;
    }

    if (filters.brand_id) {
      conditions.push(`p.brand_id = $${paramIndex}`);
      params.push(filters.brand_id);
      paramIndex++;
    }

    if (filters.search) {
      conditions.push(`p.name ILIKE $${paramIndex}`);
      params.push(`%${filters.search}%`);
      paramIndex++;
    }

    if (conditions.length > 0) {
      query += ' WHERE ' + conditions.join(' AND ');
    }

    const result = await db.query(query, params);
    return parseInt(result.rows[0].count);
  } catch (error) {
    throw error;
  }
};

/**
 * Create a new product with variants and images
 * @param {Object} productData - Product data including variants
 * @returns {Promise<Object>} Created product
 */
const createProduct = async (productData) => {
  const client = await db.connect();

  try {
    await client.query('BEGIN');

    const {
      name,
      sku,
      slug,
      description,
      category_id,
      brand_id,
      specs,
      is_published = false,
      variants = [],
      attribute_images = []
    } = productData;

    // 1. Create the main product
    const productQuery = `
      INSERT INTO products (name, sku, slug, description, category_id, brand_id, specs, is_published)
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
      RETURNING *
    `;

    const productResult = await client.query(productQuery, [
      name,
      sku || null,
      slug,
      description || null,
      category_id,
      brand_id || null,
      JSON.stringify(specs || {}),
      is_published
    ]);

    const product = productResult.rows[0];

    // 2. Create variants if provided
    if (variants && variants.length > 0) {
      for (const variant of variants) {
        const variantQuery = `
          INSERT INTO product_variants 
          (product_id, sku, variant_name, attributes, price, compare_at, cost, status)
          VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
          RETURNING id
        `;

        await client.query(variantQuery, [
          product.id,
          variant.sku,
          variant.name || null,
          JSON.stringify(variant.options || {}),
          variant.price || 0,
          variant.compare_at || null,
          variant.cost || null,
          'active'
        ]);
      }
    }

    // 4. Handle attribute-based images
    if (attribute_images && attribute_images.length > 0) {
      const cleanImages = stripBaseUrlFromImages(attribute_images);
      for (const attrImg of cleanImages) {
        await client.query(
          `INSERT INTO product_attribute_images (product_id, attribute_combo, image_urls)
           VALUES ($1, $2, $3)`,
          [product.id, JSON.stringify(attrImg.attribute_combo), attrImg.image_urls]
        );
      }
    }
    await client.query('COMMIT');

    // Return the complete product with variants
    return await getProductById(product.id);

  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
};

/**
 * Update an existing product
 * @param {string} productId - Product UUID
 * @param {Object} productData - Updated product data
 * @returns {Promise<Object>} Updated product
 */
const updateProduct = async (productId, productData) => {
  const client = await db.connect();

  try {
    await client.query('BEGIN');

    const {
      name,
      sku,
      slug,
      description,
      category_id,
      brand_id,
      specs,
      is_published,
      variants = [],
      attribute_images = []
    } = productData;

    // 1. Update the main product
    const updateQuery = `
      UPDATE products 
      SET name = $1, sku = $2, slug = $3, description = $4, category_id = $5, 
          brand_id = $6, specs = $7, is_published = $8, updated_at = now()
      WHERE id = $9
    `;

    await client.query(updateQuery, [
      name,
      sku || null,
      slug,
      description || null,
      category_id,
      brand_id || null,
      JSON.stringify(specs || {}),
      is_published,
      productId
    ]);

    // 2. Handle variants - Simple approach: Delete existing and re-insert
    // In a production app, we would match IDs to preserve them, but for now this is cleaner
    await client.query('DELETE FROM product_variants WHERE product_id = $1', [productId]);
    // Product images will be deleted due to CASCADE if they were linked to variants

    if (variants && variants.length > 0) {
      for (const variant of variants) {
        const variantQuery = `
          INSERT INTO product_variants 
          (product_id, sku, variant_name, attributes, price, compare_at, cost, status)
          VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
          RETURNING id
        `;

        await client.query(variantQuery, [
          productId,
          variant.sku,
          variant.name || null,
          JSON.stringify(variant.options || {}),
          variant.price || 0,
          variant.compare_at || null,
          variant.cost || null,
          variant.status || 'active'
        ]);
      }
    }

    // 3. Handle attribute-based images
    await client.query('DELETE FROM product_attribute_images WHERE product_id = $1', [productId]);

    if (attribute_images && attribute_images.length > 0) {
      const cleanImages = stripBaseUrlFromImages(attribute_images);
      for (const attrImg of cleanImages) {
        await client.query(
          `INSERT INTO product_attribute_images (product_id, attribute_combo, image_urls)
           VALUES ($1, $2, $3)`,
          [productId, JSON.stringify(attrImg.attribute_combo), attrImg.image_urls]
        );
      }
    }

    await client.query('COMMIT');
    return await getProductById(productId);

  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
};

module.exports = {
  getAllProducts,
  getProductById,
  getProductCount,
  createProduct,
  updateProduct
};
