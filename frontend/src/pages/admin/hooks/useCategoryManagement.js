import { useState, useEffect } from 'react';
import { Form, App } from 'antd';
import categoryService from '../../../services/category.service';

export const useCategoryManagement = () => {
    const { message } = App.useApp();
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editingCategory, setEditingCategory] = useState(null);
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);
    const [tableLoading, setTableLoading] = useState(false);
    const [categories, setCategories] = useState([]);

    const fetchCategories = async () => {
        setTableLoading(true);
        try { setCategories(await categoryService.getAllCategories()); }
        catch (e) { message.error('Không thể tải danh sách'); } finally { setTableLoading(false); }
    };

    useEffect(() => { fetchCategories(); }, []);

    const showModal = (cat = null) => { setEditingCategory(cat); setIsModalOpen(true); if (cat) form.setFieldsValue(cat); else form.resetFields(); };
    const handleCancel = () => { setIsModalOpen(false); setEditingCategory(null); };

    const handleDelete = async (id) => {
        try { await categoryService.deleteCategory(id); message.success('Thành công'); fetchCategories(); }
        catch (e) { message.error('Lỗi khi xóa'); }
    };

    const onFinish = async (v) => {
        setLoading(true);
        try {
            editingCategory ? await categoryService.updateCategory(editingCategory.id, v) : await categoryService.createCategory(v);
            message.success('Thành công!'); setIsModalOpen(false); setEditingCategory(null); form.resetFields(); fetchCategories();
        } catch (e) { message.error(e.message || 'Lỗi khi lưu'); } finally { setLoading(false); }
    };

    return { 
        categories, 
        tableLoading, 
        isModalOpen, 
        editingCategory, 
        loading, 
        form, 
        showModal, 
        handleCancel, 
        handleDelete, 
        onFinish 
    };
};
