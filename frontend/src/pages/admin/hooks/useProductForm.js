import { useState, useEffect } from 'react';
import { Form, App } from 'antd';
import { useNavigate } from 'react-router-dom';
import categoryService from '../../../services/category.service';
import productService from '../../../services/product.service';
import { useProductFormInit } from './useProductFormInit';
import { useVariantLogic } from './useVariantLogic';

export const useProductForm = (id = null) => {
    const navigate = useNavigate();
    const { message } = App.useApp();
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(!!id);
    const [submitting, setSubmitting] = useState(false);
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState(null);
    const [attributes, setAttributes] = useState([]);
    const [attributeValues, setAttributeValues] = useState({});
    const [inputValue, setInputValue] = useState({});
    const [variants, setVariants] = useState([]);
    const [selectedImageAttributes, setSelectedImageAttributes] = useState([]);
    const [imageAttributeValues, setImageAttributeValues] = useState({});
    const [attributeImages, setAttributeImages] = useState({});
    const [generalImages, setGeneralImages] = useState([]);

    useProductFormInit(id, form, message, navigate, setSelectedCategory, setAttributes, setAttributeValues, setVariants, setSelectedImageAttributes, setImageAttributeValues, setGeneralImages, setAttributeImages, setLoading);
    const { generateVariants, handleVariantChange } = useVariantLogic(form, attributes, setVariants);

    const handleCategoryChange = async (cid) => {
        const cats = categories.length ? categories : await categoryService.getAllCategories();
        if (!categories.length) setCategories(cats);
        const cat = cats.find(c => c.id === cid);
        setSelectedCategory(cat); setAttributes(cat?.attributes || []);
        setAttributeValues({}); setVariants([]); form.setFieldsValue({ attributes: {} });
    };

    const handleAttributeValueChange = (n, v, t) => {
        const next = { ...attributeValues, [n]: v };
        setAttributeValues(next); if (t === 'option') generateVariants(next);
    };

    const onFinish = async (v) => {
        try {
            setSubmitting(true);
            const slug = v.name.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd').replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
            const payload = {
                ...v, slug, specs: attributes.filter(a => a.type === 'text' && attributeValues[a.name]).reduce((s, a) => ({ ...s, [a.name]: attributeValues[a.name] }), {}),
                variants: variants.map(vr => ({ name: vr.name, sku: vr.sku, price: vr.price, stock: vr.stock, status: vr.status, options: vr.options, compare_at: null, cost: null })),
                attribute_images: [
                    ...(generalImages.length ? [{ attribute_combo: [], image_urls: generalImages }] : []),
                    ...Object.entries(attributeImages).map(([k, u]) => ({ attribute_combo: k.split('|').map((val, i) => ({ name: selectedImageAttributes[i], value: val })), image_urls: u }))
                ]
            };
            id ? await productService.updateProduct(id, payload) : await productService.createProduct(payload);
            message.success('Thành công!'); navigate('/admin/products');
        } catch (e) { message.error('Thất bại'); } finally { setSubmitting(false); }
    };

    return { 
        form, 
        loading, 
        submitting, 
        categories, 
        selectedCategory, 
        attributes, 
        attributeValues, 
        inputValue, 
        setInputValue, 
        variants, 
        selectedImageAttributes, 
        setSelectedImageAttributes, 
        imageAttributeValues, 
        setImageAttributeValues, 
        attributeImages, 
        setAttributeImages, 
        generalImages, 
        setGeneralImages, 
        handleCategoryChange, 
        handleAttributeValueChange, 
        handleVariantChange: (k, f, val) => handleVariantChange(variants, setVariants, k, f, val), 
        onFinish, 
        navigate 
    };
};
