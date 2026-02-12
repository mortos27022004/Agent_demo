import { cartesian } from '../../../utils/cartesian';

export const useVariantLogic = (form, attributes, setVariants) => {
    const generateVariants = (vals) => {
        const optAttrs = attributes.filter(a => a.type === 'option');
        const arrays = optAttrs.map(a => (vals[a.name] || []).map(v => ({ name: a.name, value: v }))).filter(arr => arr.length);
        if (!arrays.length) return setVariants([]);
        setVariants(cartesian(...arrays).map((combo, i) => {
            const arr = Array.isArray(combo) ? combo : [combo];
            return { key: `new-${i}`, name: arr.map(c => c.value).join(' - '), sku: `${form.getFieldValue('sku') || 'SKU'}-${arr.map(c => c.value.substring(0, 3).toUpperCase()).join('-')}`, price: 0, stock: 0, status: 'active', options: arr };
        }));
    };

    const handleVariantChange = (variants, setVariants, key, f, v) => {
        const next = [...variants]; const idx = next.findIndex(vr => vr.key === key);
        if (idx > -1) { next[idx][f] = v; setVariants(next); }
    };

    return { generateVariants, handleVariantChange };
};
