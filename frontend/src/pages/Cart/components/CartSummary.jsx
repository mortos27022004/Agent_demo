import React from 'react';
import { Card, Space, Typography, Divider, Button } from 'antd';
import { COLORS } from '../../../theme/colors';

const { Title, Text } = Typography;

const CartSummary = ({ total, count, formatPrice, onCheckout }) => (
    <Card title={<Title level={4} style={{ margin: 0 }}>Tóm tắt đơn hàng</Title>} style={{ borderRadius: '12px' }}>
        <Space direction="vertical" style={{ width: '100%' }} size="middle">
            <div style={{ display: 'flex', justifyContent: 'space-between' }}><Text type="secondary">Tạm tính ({count} sản phẩm):</Text><Text strong>{formatPrice(total)}</Text></div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}><Text type="secondary">Phí vận chuyển:</Text><Text type="secondary">Tính tại bước tiếp theo</Text></div>
            <Divider style={{ margin: '8px 0' }} />
            <div style={{ display: 'flex', justifyContent: 'space-between' }}><Title level={4} style={{ margin: 0 }}>Tổng cộng:</Title><Title level={3} style={{ margin: 0, color: COLORS.PRIMARY }}>{formatPrice(total)}</Title></div>
            <Text type="secondary" style={{ fontSize: '12px', textAlign: 'right', display: 'block' }}>(Đã bao gồm VAT nếu có)</Text>
            <Button type="primary" size="large" block style={{ height: '50px', borderRadius: '8px', fontSize: '18px', fontWeight: 'bold' }} onClick={onCheckout}>TIẾN HÀNH THANH TOÁN</Button>
            <Card style={{ backgroundColor: '#f9f9f9' }} bodyStyle={{ padding: '12px' }}>
                <Space direction="vertical" size="small">
                    <Text strong style={{ fontSize: '13px' }}>Chính sách giỏ hàng:</Text>
                    <Text type="secondary" style={{ fontSize: '12px' }}>• Giá sản phẩm có thể thay đổi</Text>
                    <Text type="secondary" style={{ fontSize: '12px' }}>• Giỏ hàng lưu tự động</Text>
                </Space>
            </Card>
        </Space>
    </Card>
);

export default CartSummary;
