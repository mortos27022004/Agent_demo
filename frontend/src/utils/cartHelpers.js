export const handleGuestAdd = (prev, product, variant, quantity) => {
    const existing = prev.find(i => i.variant_id === variant.id);
    if (existing) return prev.map(i => i.variant_id === variant.id ? { ...i, quantity: i.quantity + quantity } : i);
    return [...prev, { variant_id: variant.id, product_id: product.id, product_name: product.name, product_slug: product.slug, variant_name: variant.variant_name, price: variant.price, image_url: product.image_url || (product.images?.[0]), quantity }];
};

export const handleGuestUpdate = (prev, variantId, newQuantity) => prev.map(i => i.variant_id === variantId ? { ...i, quantity: newQuantity } : i);

export const handleGuestRemove = (prev, variantId) => prev.filter(i => i.variant_id !== variantId);
