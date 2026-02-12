import React from 'react';
import { Card, Typography, Divider, Space } from 'antd';
import { COLORS } from '../../../theme/colors';

const { Title, Text } = Typography;

const OrderSummary = ({ cartItems, cartTotal, formatPrice }) => {
    return (
        <Card title="Đơn hàng của bạn" style={{ borderRadius: '12px' }}>
            <div style={{ maxHeight: '300px', overflowY: 'auto', marginBottom: '16px' }}>
                {cartItems.map(item => (
                    <div key={item.variant_id} style={{ display: 'flex', marginBottom: '12px', gap: '12px' }}>
                        <img
                            src={item.image_url}
                            alt={item.product_name}
                            style={{ width: '50px', height: '50px', objectFit: 'cover', borderRadius: '4px' }}
                        />
                        <div style={{ flex: 1 }}>
                            <Text strong style={{ fontSize: '13px', display: 'block' }}>{item.product_name}</Text>
                            <Text type="secondary" style={{ fontSize: '12px' }}>SL: {item.quantity}</Text>
                        </div>
                        <Text strong>{formatPrice(item.price * item.quantity)}</Text>
                    </div>
                ))}
            </div>
            <Divider />
            <Space direction="vertical" style={{ width: '100%' }} size="small">
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Text type="secondary">Tạm tính:</Text>
                    <Text>{formatPrice(cartTotal)}</Text>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Text type="secondary">Phí vận chuyển:</Text>
                    <Text>{formatPrice(30000)}</Text>
                </div>
                <Divider style={{ margin: '8px 0' }} />
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Title level={4} style={{ margin: 0 }}>Tổng cộng:</Title>
                    <Title level={4} style={{ margin: 0, color: COLORS.PRIMARY }}>{formatPrice(cartTotal + 30000)}</Title>
                </div>
            </Space>
        </Card>
    );
};

export default OrderSummary;
