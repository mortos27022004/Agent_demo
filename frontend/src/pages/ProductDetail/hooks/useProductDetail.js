import { useState, useEffect, useMemo } from 'react';
import { App } from 'antd';
import { useNavigate } from 'react-router-dom';
import productService from '../../../services/product.service';

export const useProductDetail = (id) => {
    const navigate = useNavigate();
    const { message } = App.useApp();
    const [loading, setLoading] = useState(true);
    const [product, setProduct] = useState(null);
    const [selectedVariant, setSelectedVariant] = useState(null);
    const [selectedOptions, setSelectedOptions] = useState({});
    const [imageIndex, setImageIndex] = useState(0);

    const activeImageSet = useMemo(() => {
        if (!product) return [];
        const match = (product.attribute_images || []).find(ai =>
            ai.attribute_combo?.length > 0 && ai.attribute_combo.every(c => selectedOptions[c.name] === c.value)
        );
        if (match?.image_urls?.length > 0) return match.image_urls;

        const general = (product.attribute_images || []).find(ai => !ai.attribute_combo?.length);
        if (general?.image_urls?.length > 0) return general.image_urls;

        return product.main_image ? [product.main_image] : [];
    }, [product, selectedOptions]);

    useEffect(() => {
        if (activeImageSet.length > 0 && imageIndex >= activeImageSet.length) setImageIndex(0);
    }, [activeImageSet, imageIndex]);

    useEffect(() => {
        const fetchDetail = async () => {
            try {
                setLoading(true);
                const data = await productService.getProductById(id);
                if (!data) { message.error('Không tìm thấy sản phẩm'); navigate('/'); return; }
                setProduct(data);
                if (data.variants?.length > 0) {
                    const first = data.variants[0];
                    setSelectedVariant(first);
                    const options = {};
                    const attrs = Array.isArray(first.attributes) ? first.attributes : Object.entries(first.attributes || {}).map(([n, v]) => ({ name: n, value: v }));
                    attrs.forEach(a => options[a.name] = a.value);
                    setSelectedOptions(options);
                }
                setImageIndex(0);
            } catch (e) { message.error('Lỗi khi tải thông tin'); } finally { setLoading(false); }
        };
        fetchDetail();
    }, [id, message, navigate]);

    const allOptions = useMemo(() => {
        if (!product?.variants) return {};
        const groups = {};
        product.variants.forEach(v => {
            const attrs = Array.isArray(v.attributes) ? v.attributes : Object.entries(v.attributes || {}).map(([n, val]) => ({ name: n, value: val }));
            attrs.forEach(a => { if (!groups[a.name]) groups[a.name] = new Set(); groups[a.name].add(a.value); });
        });
        const result = {};
        Object.entries(groups).forEach(([n, v]) => result[n] = Array.from(v).sort());
        return result;
    }, [product]);

    const handleOptionChange = (n, v) => {
        const next = { ...selectedOptions, [n]: v };
        setSelectedOptions(next);
        const match = product.variants.find(varnt => {
            const vAttrs = Array.isArray(varnt.attributes) ? varnt.attributes : Object.entries(varnt.attributes || {}).map(([nm, val]) => ({ name: nm, value: val }));
            return vAttrs.every(a => next[a.name] === a.value);
        });
        if (match) setSelectedVariant(match);
    };

    return { loading, product, selectedVariant, selectedOptions, activeImageSet, imageIndex, setImageIndex, allOptions, handleOptionChange };
};
