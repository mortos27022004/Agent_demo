import React from 'react';
import { Typography, Card, Breadcrumb, Empty, Button, Spin, Space } from 'antd';
import { HomeOutlined } from '@ant-design/icons';
import { useNavigate, Link } from 'react-router-dom';
import MainLayout from '../../components/layout/MainLayout';
import OrderTable from './components/OrderTable';
import { useOrders } from './hooks/useOrders';

const { Title, Text } = Typography;

const OrdersPage = () => {
    const navigate = useNavigate();
    const { orders, loading, formatPrice } = useOrders();

    return (
        <MainLayout>
            <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto', minHeight: '80vh' }}>
                <Breadcrumb style={{ marginBottom: 24 }} items={[{ title: <Link to="/"><HomeOutlined /> Trang chủ</Link> }, { title: 'Đơn hàng của tôi' }]} />
                <Title level={2} style={{ marginBottom: 32 }}>Đơn hàng của tôi</Title>
                {loading ? (
                    <div style={{ textAlign: 'center', padding: '100px' }}><Spin size="large" /></div>
                ) : orders.length === 0 ? (
                    <Card style={{ textAlign: 'center', padding: '64px 0', borderRadius: '12px' }}>
                        <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={<Space direction="vertical"><Text type="secondary">Bạn chưa có đơn hàng nào</Text><Button type="primary" onClick={() => navigate('/')}>MUA SẮM NGAY</Button></Space>} />
                    </Card>
                ) : (
                    <Card style={{ borderRadius: '12px' }} bodyStyle={{ padding: 0 }}>
                        <OrderTable orders={orders} navigate={navigate} formatPrice={formatPrice} />
                    </Card>
                )}
            </div>
        </MainLayout>
    );
};

export default OrdersPage;
