import React from 'react';
import { Button, Typography } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import CategoryTable from './components/CategoryTable';
import CategoryModal from './components/CategoryModal';
import { useCategoryManagement } from './hooks/useCategoryManagement';

const { Title } = Typography;

const CategoryManagement = () => {
    const { categories, tableLoading, isModalOpen, editingCategory, loading, form, showModal, handleCancel, handleDelete, onFinish } = useCategoryManagement();

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                <Title level={2} style={{ margin: 0 }}>Quản lý danh mục</Title>
                <Button type="primary" icon={<PlusOutlined />} size="large" onClick={() => showModal()} style={{ borderRadius: '8px', height: '45px' }}>Thêm danh mục mới</Button>
            </div>
            <CategoryTable categories={categories} loading={tableLoading} onEdit={showModal} onDelete={handleDelete} />
            <CategoryModal open={isModalOpen} onCancel={handleCancel} editingCategory={editingCategory} form={form} onFinish={onFinish} loading={loading} />
        </div>
    );
};

export default CategoryManagement;
