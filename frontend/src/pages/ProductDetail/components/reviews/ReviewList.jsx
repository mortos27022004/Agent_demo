import React from 'react';
import { List, Avatar, Space, Tag, Typography, Rate } from 'antd';
import { UserOutlined, CheckCircleFilled } from '@ant-design/icons';

const { Text, Paragraph } = Typography;

const ReviewList = ({ reviews, loading }) => (
    <List loading={loading} itemLayout="horizontal" dataSource={reviews} renderItem={(item) => (
        <List.Item>
            <List.Item.Meta avatar={<Avatar icon={<UserOutlined />} />} title={
                <Space direction="vertical" size={0}>
                    <Space><Text strong>{item.user_name}</Text>{item.is_verified_purchase && <Tag color="success" icon={<CheckCircleFilled />}>Đã mua hàng</Tag>}</Space>
                    <Rate disabled value={item.rating} style={{ fontSize: 12 }} />
                </Space>
            } description={
                <div style={{ marginTop: 8 }}>
                    <Paragraph style={{ color: '#333' }}>{item.comment}</Paragraph>
                    <Text type="secondary" style={{ fontSize: 12 }}>{new Date(item.created_at).toLocaleDateString('vi-VN')}</Text>
                </div>
            } />
        </List.Item>
    )} />
);

export default ReviewList;
