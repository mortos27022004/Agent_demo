import React from 'react';
import { Row, Col, Typography, Button, Card, Empty, Breadcrumb, Space } from 'antd';
import { HomeOutlined, ShoppingCartOutlined } from '@ant-design/icons';
import { useNavigate, Link } from 'react-router-dom';
import MainLayout from '../../components/layout/MainLayout';
import { useCart } from '../../context/CartContext';
import CartItemList from './components/CartItemList';
import CartSummary from './components/CartSummary';

const { Title, Text } = Typography;

const CartPage = () => {
    const navigate = useNavigate();
    const { cartItems, updateQuantity, removeFromCart, cartTotal, cartCount } = useCart();
    const formatPrice = (p) => new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p || 0);

    return (
        <MainLayout>
            <div style={{ padding: '24px', maxWidth: '1400px', margin: '0 auto', minHeight: '80vh' }}>
                <Breadcrumb style={{ marginBottom: 24 }} items={[{ title: <Link to="/"><HomeOutlined /> Trang chủ</Link> }, { title: 'Giỏ hàng' }]} />
                <Title level={2} style={{ marginBottom: 32 }}><ShoppingCartOutlined /> Giỏ hàng ({cartCount} sản phẩm)</Title>
                {cartItems.length === 0 ? (
                    <Card style={{ textAlign: 'center', padding: '64px 0', borderRadius: '12px' }}>
                        <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={<Space direction="vertical"><Text type="secondary" style={{ fontSize: '16px' }}>Giỏ hàng của bạn đang trống</Text><Button type="primary" size="large" onClick={() => navigate('/')}>TIẾP TỤC MUA SẮM</Button></Space>} />
                    </Card>
                ) : (
                    <Row gutter={24}>
                        <Col xs={24} lg={16}><Card style={{ borderRadius: '12px', overflow: 'hidden' }} bodyStyle={{ padding: 0 }}><CartItemList items={cartItems} updateQuantity={updateQuantity} removeFromCart={removeFromCart} formatPrice={formatPrice} /></Card></Col>
                        <Col xs={24} lg={8}><CartSummary total={cartTotal} count={cartCount} formatPrice={formatPrice} onCheckout={() => navigate('/checkout')} /></Col>
                    </Row>
                )}
            </div>
        </MainLayout>
    );
};

export default CartPage;
