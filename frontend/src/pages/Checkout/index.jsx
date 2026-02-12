import React, { useEffect } from 'react';
import { Row, Col, Typography, Card, Form, Breadcrumb, Steps, Result, Button } from 'antd';
import { HomeOutlined, CreditCardOutlined } from '@ant-design/icons';
import { Link } from 'react-router-dom';
import MainLayout from '../../components/layout/MainLayout';
import OrderSummary from './components/OrderSummary';
import CheckoutForms from './components/CheckoutForms';
import { useCheckoutLogic } from './hooks/useCheckoutLogic';

const { Title } = Typography;

const CheckoutPage = () => {
    const { navigate, cartItems, cartTotal, currentStep, setCurrentStep, loading, isSuccess, orderInfo, onFinish } = useCheckoutLogic();
    const [form] = Form.useForm();
    const formatPrice = (p) => new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p || 0);

    useEffect(() => { if (cartItems.length === 0 && !isSuccess) navigate('/cart'); }, [cartItems, navigate, isSuccess]);

    if (isSuccess) return (
        <MainLayout>
            <div style={{ padding: '64px 24px', maxWidth: '800px', margin: '0 auto' }}>
                <Result status="success" title="Đặt hàng thành công!" subTitle={`Mã đơn hàng: ${orderInfo?.order_code}`}
                    extra={[<Button type="primary" key="h" onClick={() => navigate('/')}>Tiếp tục mua sắm</Button>, <Button key="o" onClick={() => navigate('/orders')}>Xem đơn hàng</Button>]} />
            </div>
        </MainLayout>
    );

    const steps = [{ title: 'Thông tin nhận hàng', icon: <HomeOutlined /> }, { title: 'Thanh toán', icon: <CreditCardOutlined /> }];

    return (
        <MainLayout>
            <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto', minHeight: '80vh' }}>
                <Breadcrumb style={{ marginBottom: 24 }} items={[{ title: <Link to="/"><HomeOutlined /> Trang chủ</Link> }, { title: <Link to="/cart">Giỏ hàng</Link> }, { title: 'Thanh toán' }]} />
                <Title level={2} style={{ marginBottom: 32 }}>Thanh toán</Title>
                <Row gutter={24}>
                    <Col xs={24} lg={16}>
                        <Card style={{ borderRadius: '12px', marginBottom: '24px' }}>
                            <Steps current={currentStep} items={steps} style={{ marginBottom: '32px' }} />
                            <Form form={form} layout="vertical" onFinish={onFinish} initialValues={{ payment_method: 'cod' }}>
                                <CheckoutForms currentStep={currentStep} setCurrentStep={setCurrentStep} form={form} loading={loading} />
                            </Form>
                        </Card>
                    </Col>
                    <Col xs={24} lg={8}><OrderSummary cartItems={cartItems} cartTotal={cartTotal} formatPrice={formatPrice} /></Col>
                </Row>
            </div>
        </MainLayout>
    );
};

export default CheckoutPage;
