import { useState, useEffect } from 'react';
import { App } from 'antd';
import productService from '../../../services/product.service';

export const useProductManagement = () => {
    const { message } = App.useApp();
    const [searchText, setSearchText] = useState('');
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(false);

    const fetchProducts = async () => {
        setLoading(true);
        try {
            const data = await productService.getAllProducts();
            setProducts(data.products || []);
        } catch (e) {
            message.error('Không thể tải danh sách sản phẩm');
            setProducts([]);
        } finally { setLoading(false); }
    };

    useEffect(() => { fetchProducts(); }, []);

    const filteredProducts = products.filter(p =>
        p.name.toLowerCase().includes(searchText.toLowerCase()) ||
        p.sku?.toLowerCase().includes(searchText.toLowerCase())
    );

    return { searchText, setSearchText, products: filteredProducts, loading, fetchProducts };
};
