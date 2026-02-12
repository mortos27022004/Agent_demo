import React from 'react';
import { Card, Typography, List, Button, Space, Tag } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import userService from '../../../services/user.service';

const { Title, Text } = Typography;

const AddressBook = ({ addresses, setIsAddressModalOpen, fetchProfile }) => {
    return (
        <Card bordered={false}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 24 }}>
                <Title level={4} style={{ margin: 0 }}>Địa chỉ của tôi</Title>
                <Button type="primary" icon={<PlusOutlined />} onClick={() => setIsAddressModalOpen(true)}>Thêm địa chỉ mới</Button>
            </div>
            <List
                dataSource={addresses || []}
                renderItem={(item) => (
                    <List.Item
                        actions={[
                            <Button type="link" danger onClick={() => userService.removeAddress(item.id).then(fetchProfile)}>Xóa</Button>
                        ]}
                    >
                        <List.Item.Meta
                            title={
                                <Space>
                                    <Text strong>{item.recipient}</Text>
                                    <Text type="secondary">({item.phone})</Text>
                                    {item.is_default && <Tag color="blue">Mặc định</Tag>}
                                </Space>
                            }
                            description={item.line1}
                        />
                    </List.Item>
                )}
            />
        </Card>
    );
};

export default AddressBook;
