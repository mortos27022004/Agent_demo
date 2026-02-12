import { useState, useEffect } from 'react';
import { Menu, Spin, Alert } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';
import categoryService from '../../services/category.service';
import { categoryIcons } from './categoryIcons.jsx';

const CategorySidebar = ({ mode = 'inline' }) => {
    const [categories, setCategories] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => { fetchCategories(); }, []);

    const fetchCategories = async () => {
        try { setLoading(true); setCategories(await categoryService.getAllCategories()); setError(null); }
        catch (err) { console.error(err); setError('Không thể tải danh mục.'); }
        finally { setLoading(false); }
    };

    const items = categories.map((cat) => ({ key: cat.id, icon: categoryIcons[cat.icon] || <InfoCircleOutlined />, label: cat.name }));

    if (loading) return <div style={{ padding: '20px', textAlign: 'center' }}><Spin tip="Đang tải..."><div style={{ height: 50 }} /></Spin></div>;
    if (error) return <Alert message="Lỗi" description={error} type="error" showIcon style={{ margin: '10px' }} />;

    return (
        <Menu mode={mode} items={items} onClick={(e) => console.log('Clicked:', e.key)}
            style={{ border: 'none' }} />
    );
};

export default CategorySidebar;
