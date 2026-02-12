import React from 'react';
import { Card, Typography, Button, Row, Col } from 'antd';
import { EditOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

const PersonalInfo = ({ user, setIsEditModalOpen }) => {
    return (
        <Card bordered={false}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 24 }}>
                <Title level={4} style={{ margin: 0 }}>Thông tin cá nhân</Title>
                <Button icon={<EditOutlined />} onClick={() => setIsEditModalOpen(true)}>Chỉnh sửa</Button>
            </div>
            <Row gutter={[16, 24]}>
                <Col span={12}>
                    <Text type="secondary">Họ và tên</Text>
                    <div style={{ fontSize: '16px', fontWeight: '500' }}>{user?.full_name}</div>
                </Col>
                <Col span={12}>
                    <Text type="secondary">Email</Text>
                    <div style={{ fontSize: '16px', fontWeight: '500' }}>{user?.email}</div>
                </Col>
                <Col span={12}>
                    <Text type="secondary">Số điện thoại</Text>
                    <div style={{ fontSize: '16px', fontWeight: '500' }}>{user?.phone || 'Chưa cập nhật'}</div>
                </Col>
                <Col span={12}>
                    <Text type="secondary">Giới tính</Text>
                    <div style={{ fontSize: '16px', fontWeight: '500' }}>{user?.gender === 'male' ? 'Nam' : user?.gender === 'female' ? 'Nữ' : 'Khác'}</div>
                </Col>
            </Row>
        </Card>
    );
};

export default PersonalInfo;
