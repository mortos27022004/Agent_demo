import { useState, useEffect } from 'react';
import categoryService from '../../../services/category.service';
import productService from '../../../services/product.service';

export const useProductFormInit = (id, form, message, navigate, setSelectedCategory, setAttributes, setAttributeValues, setVariants, setSelectedImageAttributes, setImageAttributeValues, setGeneralImages, setAttributeImages, setLoading) => {
    useEffect(() => {
        const init = async () => {
            try {
                const cats = await categoryService.getAllCategories();
                if (!id) return;
                const prod = await productService.getProductById(id);
                if (!prod) { navigate('/admin/products'); return; }
                form.setFieldsValue({ name: prod.name, sku: prod.sku, description: prod.description, category_id: prod.category_id, status: prod.is_published ? 'active' : 'inactive' });
                const cat = cats.find(c => c.id === prod.category_id);
                if (cat) {
                    setSelectedCategory(cat); setAttributes(cat.attributes || []);
                    const attrVals = {}; (prod.variants || []).forEach(v => (v.attributes || []).forEach(a => { if (a.name && a.value) { if (!attrVals[a.name]) attrVals[a.name] = []; if (!attrVals[a.name].includes(a.value)) attrVals[a.name].push(a.value); } }));
                    Object.entries(prod.specs || {}).forEach(([n, v]) => attrVals[n] = v); setAttributeValues(attrVals);
                    setVariants((prod.variants || []).map((v, i) => ({ key: v.id || i, name: v.variant_name, sku: v.sku, price: parseFloat(v.price), stock: v.stock, status: v.status, options: v.attributes })));
                    const attrImgs = {}; const gens = []; let firstC = null; let keys = [];
                    (prod.attribute_images || []).forEach(ai => {
                        if (!ai.attribute_combo?.length) gens.push(...ai.image_urls);
                        else {
                            const curKeys = ai.attribute_combo.map(c => c.name);
                            if (!keys.length) { keys = curKeys; setSelectedImageAttributes(curKeys); firstC = ai.attribute_combo.reduce((acc, c) => ({ ...acc, [c.name]: c.value }), {}); }
                            attrImgs[keys.map(k => ai.attribute_combo.find(c => c.name === k).value).join('|')] = ai.image_urls;
                        }
                    });
                    setGeneralImages(gens); setAttributeImages(attrImgs); if (firstC) setImageAttributeValues(firstC);
                }
            } catch (e) { message.error('Lỗi'); } finally { setLoading(false); }
        };
        init();
    }, [id]);
};
