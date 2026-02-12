import React from 'react';
import { Typography, Form, Rate, Input, Button, Card, message } from 'antd';

const { Title, Text } = Typography;
const { TextArea } = Input;

const ReviewForm = ({ user, form, onFinish, submitting }) => (
    <div>
        <Title level={4}>Gửi nhận xét của bạn</Title>
        {user ? (
            <Form form={form} onFinish={onFinish} layout="vertical">
                <Form.Item name="rating" label="Đánh giá của bạn" rules={[{ required: true, message: 'Vui lòng chọn mức đánh giá' }]}><Rate /></Form.Item>
                <Form.Item name="comment" label="Nội dung nhận xét" rules={[{ required: true, message: 'Vui lòng nhập nội dung' }]}><TextArea rows={4} placeholder="Chia sẻ trải nghiệm..." /></Form.Item>
                <Button type="primary" htmlType="submit" loading={submitting} size="large">Gửi đánh giá</Button>
            </Form>
        ) : (
            <Card type="inner" style={{ textAlign: 'center', background: '#f5f5f5' }}>
                <Text>Vui lòng <Text strong underline style={{ cursor: 'pointer' }} onClick={() => message.info('Vui lòng đăng nhập')}>đăng nhập</Text> để gửi nhận xét.</Text>
            </Card>
        )}
    </div>
);

export default ReviewForm;
