/**
 * Transform product data from backend format to frontend format
 * @param {Object} product - Product from backend API
 * @returns {Object} Transformed product for ProductCard
 */
export const transformProduct = (product) => {
    // Get the first variant's pricing information
    const firstVariant = product.variants && product.variants[0];
    const price = firstVariant?.price || 0;
    const compareAt = firstVariant?.compare_at || price;

    // Calculate discount percentage
    const discountPercent = compareAt > price
        ? Math.round(((compareAt - price) / compareAt) * 100)
        : 0;

    // Get first variant's image or product main image
    const imageUrl = firstVariant?.image || product.main_image || '/placeholder.jpg';

    // Extract specs from variant attributes or product specs
    const rawAttributes = firstVariant?.attributes || {};

    // Convert array format [{name, value}] to object format {key: value}
    let attributes = {};
    if (Array.isArray(rawAttributes)) {
        // Backend returns attributes as array: [{name: "CPU", value: "i5"}, ...]
        rawAttributes.forEach(attr => {
            if (attr.name && attr.value) {
                attributes[attr.name] = attr.value;
            }
        });
    } else if (typeof rawAttributes === 'object') {
        // Already in object format
        attributes = rawAttributes;
    }

    // Map common attribute names to standardized keys
    const specs = {
        color: attributes['Màu sắc'] || attributes.color || attributes['Color'] || 'N/A',
        cpu: attributes.cpu || attributes.CPU || attributes['Chip'] || 'N/A',
        ram: attributes.ram || attributes.RAM || 'N/A',
        storage: attributes.ssd || attributes.storage || attributes['Ổ cứng'] || attributes['Bộ nhớ'] || 'N/A',
        gpu: attributes.gpu || attributes['Card đồ họa'] || 'N/A'
    };

    const result = {
        id: product.id,
        name: product.name,
        priceOriginal: compareAt,
        priceSale: price,
        discountPercent: discountPercent,
        rating: 4.5, // Default rating - TODO: implement ratings system
        specs: specs,
        image: imageUrl,
        slug: product.slug,
        category: product.category_name,
        brand: product.brand_name
    };

    // Debug: Log product and specs to check data
    console.log('TransformProduct:', {
        productName: product.name,
        rawAttributes: firstVariant?.attributes,
        convertedAttributes: attributes,
        specs: specs,
        variantImage: firstVariant?.image,
        productMainImage: product.main_image,
        finalImageUrl: imageUrl
    });

    return result;
};

/**
 * Transform categories from backend format to sidebar format
 * @param {Array} categories - Categories from backend API
 * @returns {Array} Transformed categories
 */
export const transformCategories = (categories) => {
    return categories.map(cat => ({
        id: cat.id,
        name: cat.name,
        slug: cat.slug,
        icon: cat.icon || 'info-circle', // Default icon
        product_count: cat.product_count || 0
    }));
};
