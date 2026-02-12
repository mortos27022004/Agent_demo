import React from 'react';
import { Row, Col, Card, Statistic } from 'antd';
import { ShoppingCartOutlined, UserOutlined, ShoppingOutlined, DollarOutlined } from '@ant-design/icons';

const AdminDashboard = () => {
    return (
        <div>
            <h1 style={{ marginBottom: '24px' }}>Tổng quan hệ thống</h1>
            <Row gutter={[16, 16]}>
                <Col xs={24} sm={12} lg={6}>
                    <Card variant="borderless" style={{ boxShadow: '0 1px 2px 0 rgba(0,0,0,0.03), 0 1px 6px -1px rgba(0,0,0,0.02), 0 2px 4px 0 rgba(0,0,0,0.02)' }}>
                        <Statistic
                            title="Tổng đơn hàng"
                            value={128}
                            prefix={<ShoppingCartOutlined style={{ color: '#1890ff' }} />}
                        />
                    </Card>
                </Col>
                <Col xs={24} sm={12} lg={6}>
                    <Card variant="borderless" style={{ boxShadow: '0 1px 2px 0 rgba(0,0,0,0.03), 0 1px 6px -1px rgba(0,0,0,0.02), 0 2px 4px 0 rgba(0,0,0,0.02)' }}>
                        <Statistic
                            title="Khách hàng"
                            value={932}
                            prefix={<UserOutlined style={{ color: '#52c41a' }} />}
                        />
                    </Card>
                </Col>
                <Col xs={24} sm={12} lg={6}>
                    <Card variant="borderless" style={{ boxShadow: '0 1px 2px 0 rgba(0,0,0,0.03), 0 1px 6px -1px rgba(0,0,0,0.02), 0 2px 4px 0 rgba(0,0,0,0.02)' }}>
                        <Statistic
                            title="Sản phẩm"
                            value={45}
                            prefix={<ShoppingOutlined style={{ color: '#fb8c00' }} />}
                        />
                    </Card>
                </Col>
                <Col xs={24} sm={12} lg={6}>
                    <Card variant="borderless" style={{ boxShadow: '0 1px 2px 0 rgba(0,0,0,0.03), 0 1px 6px -1px rgba(0,0,0,0.02), 0 2px 4px 0 rgba(0,0,0,0.02)' }}>
                        <Statistic
                            title="Doanh thu"
                            value={154200000}
                            prefix={<DollarOutlined style={{ color: '#f5222d' }} />}
                            suffix="đ"
                        />
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default AdminDashboard;
