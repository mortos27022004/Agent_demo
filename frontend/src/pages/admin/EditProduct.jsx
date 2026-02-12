import React from 'react';
import { Form, Button, Typography, Space, Spin, App } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { useNavigate, useParams } from 'react-router-dom';
import productService from '../../services/product.service';
import BasicInfoSection from './components/product-form/BasicInfoSection';
import AttributeManager from './components/product-form/AttributeManager';
import ImageUploadSection from './components/product-form/ImageUploadSection';
import VariantTable from './components/product-form/VariantTable';
import { useProductForm } from './hooks/useProductForm';

const { Title } = Typography;

const EditProduct = () => {
    const { id } = useParams();
    const { message } = App.useApp();
    const { form, loading, submitting, categories, selectedCategory, attributes, attributeValues, inputValue, setInputValue, variants, selectedImageAttributes, setSelectedImageAttributes, imageAttributeValues, setImageAttributeValues, attributeImages, setAttributeImages, generalImages, setGeneralImages, handleCategoryChange, handleAttributeValueChange, handleVariantChange, onFinish, navigate } = useProductForm(id);

    if (loading) return <div style={{ padding: '100px', textAlign: 'center' }}><Spin size="large" tip="Đang tải dữ liệu..." /></div>;

    return (
        <div style={{ paddingBottom: 60 }}>
            <div style={{ marginBottom: 24, display: 'flex', alignItems: 'center' }}>
                <Button icon={<ArrowLeftOutlined />} onClick={() => navigate('/admin/products')} style={{ marginRight: 16, border: 'none', background: 'transparent' }} />
                <Title level={2} style={{ margin: 0 }}>Chỉnh sửa sản phẩm</Title>
            </div>
            <Form form={form} layout="vertical" onFinish={onFinish}>
                <BasicInfoSection categories={categories} onCategoryChange={handleCategoryChange} />
                <AttributeManager selectedCategory={selectedCategory} attributes={attributes} attributeValues={attributeValues} inputValue={inputValue} setInputValue={setInputValue} onAttributeValueChange={handleAttributeValueChange} />
                <ImageUploadSection attributes={attributes} attributeValues={attributeValues} generalImages={generalImages} setGeneralImages={setGeneralImages} selectedImageAttributes={selectedImageAttributes} setSelectedImageAttributes={setSelectedImageAttributes} imageAttributeValues={imageAttributeValues} setImageAttributeValues={setImageAttributeValues} attributeImages={attributeImages} setAttributeImages={setAttributeImages} onUploadImage={productService.uploadImage} message={message} />
                <VariantTable variants={variants} onVariantChange={handleVariantChange} />
                <div style={{ position: 'fixed', bottom: 0, right: 0, width: '100%', padding: '16px 24px', background: '#fff', borderTop: '1px solid #e8e8e8', display: 'flex', justifyContent: 'flex-end', zIndex: 100 }}>
                    <Space>
                        <Button size="large" onClick={() => navigate('/admin/products')} disabled={submitting}>Hủy bỏ</Button>
                        <Button type="primary" htmlType="submit" size="large" loading={submitting}>Cập nhật sản phẩm</Button>
                    </Space>
                </div>
            </Form>
        </div>
    );
};

export default EditProduct;
