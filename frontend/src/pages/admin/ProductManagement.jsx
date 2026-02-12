import React from 'react';
import { Card, Input, Typography, Button } from 'antd';
import { PlusOutlined, SearchOutlined } from '@ant-design/icons';
import ProductTable from './components/ProductTable';
import { useProductManagement } from './hooks/useProductManagement';
import { useNavigate } from 'react-router-dom';

const { Title } = Typography;

const ProductManagement = () => {
    const navigate = useNavigate();
    const { searchText, setSearchText, products, loading } = useProductManagement();

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                <Title level={2} style={{ margin: 0 }}>Quản lý sản phẩm</Title>
                <Button type="primary" icon={<PlusOutlined />} size="large" onClick={() => navigate('/admin/products/new')} style={{ height: '45px', borderRadius: '8px' }}>
                    Thêm sản phẩm mới
                </Button>
            </div>

            <Card style={{ marginBottom: '16px', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.05)' }}>
                <Input
                    placeholder="Tìm kiếm sản phẩm theo tên hoặc SKU..."
                    prefix={<SearchOutlined style={{ color: '#bfbfbf' }} />}
                    value={searchText}
                    onChange={(e) => setSearchText(e.target.value)}
                    style={{ width: '100%', maxWidth: '400px', borderRadius: '8px' }}
                    size="large"
                />
            </Card>

            <ProductTable products={products} loading={loading} navigate={navigate} />
        </div>
    );
};

export default ProductManagement;
