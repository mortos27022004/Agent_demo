import React from 'react';
import { Modal, Form, Input, Select, Button, Space, Row, Col, Typography } from 'antd';
import { PlusOutlined, MinusCircleOutlined } from '@ant-design/icons';
import { categoryIcons } from '../../../components/sidebar/categoryIcons.jsx';

const { Title, Text } = Typography;
const { Option } = Select;

const CategoryModal = ({ open, onCancel, editingCategory, form, onFinish, loading }) => (
    <Modal title={<Title level={4}>{editingCategory ? 'Chỉnh sửa danh mục' : 'Thêm danh mục mới'}</Title>} open={open} onCancel={onCancel} footer={null} centered destroyOnHidden width={650}>
        <Form form={form} layout="vertical" onFinish={onFinish} initialValues={{ status: 'active', icon: 'info-circle', attributes: [] }} style={{ marginTop: '20px' }}>
            <Form.Item
                name="name"
                label="Tên danh mục"
                rules={[{ required: true }]}
            ><Input placeholder="Ví dụ: Laptop Gaming" size="large" /></Form.Item>
            <Form.Item
                name="slug"
                label="Slug"
                rules={[{ required: true }]}
            ><Input placeholder="Ví dụ: laptop-gaming" size="large" /></Form.Item>
            <Row gutter={16}>
                <Col span={12}>
                    <Form.Item
                        name="icon"
                        label="Biểu tượng"
                        rules={[{ required: true }]}
                    >
                        <Select size="large" placeholder="Chọn icon">
                            {Object.entries(categoryIcons).map(([key, icon]) => (
                                <Option key={key} value={key}>
                                    <Space>
                                        {icon}
                                        <span>{key}</span>
                                    </Space>
                                </Option>
                            ))}
                        </Select>
                    </Form.Item>
                </Col>
                <Col span={12}>
                    <Form.Item
                        name="status"
                        label="Trạng thái"
                    >
                        <Select size="large">
                            <Option value="active">Hoạt động</Option>
                            <Option value="inactive">Tạm ngưng</Option>
                        </Select>
                    </Form.Item>
                </Col>
            </Row>
            <div style={{ marginBottom: '24px' }}>
                <Text strong style={{ display: 'block', marginBottom: '12px' }}>Thuộc tính đặc trưng</Text>
                <Form.List name="attributes">
                    {(fields, { add, remove }) => (
                        <>
                            {fields.map(({ key, name, ...rest }) => (
                                <Row key={key} gutter={12} align="middle" style={{ marginBottom: 12 }}>
                                    <Col flex="auto"><Form.Item {...rest} name={[name, 'name']} rules={[{ required: true }]} style={{ marginBottom: 0 }}><Input placeholder="Tên (VD: RAM)" size="large" /></Form.Item></Col>
                                    <Col flex="180px"><Form.Item {...rest} name={[name, 'type']} rules={[{ required: true }]} style={{ marginBottom: 0 }}>
                                        <Select placeholder="Kiểu" size="large">
                                            <Option value="text">Văn bản</Option>
                                            <Option value="option">Lựa chọn</Option>
                                        </Select>
                                    </Form.Item></Col>
                                    <Col flex="32px"><MinusCircleOutlined onClick={() => remove(name)} style={{ color: '#ff4d4f', fontSize: '20px', cursor: 'pointer' }} /></Col>
                                </Row>
                            ))}
                            <Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />} size="large">Thêm thuộc tính</Button>
                        </>
                    )}
                </Form.List>
            </div>
            <Form.Item style={{ marginBottom: 0, display: 'flex', justifyContent: 'flex-end' }}>
                <Space size="middle"><Button onClick={onCancel} size="large">Hủy</Button><Button type="primary" htmlType="submit" size="large" loading={loading} style={{ borderRadius: '8px', padding: '0 32px' }}>{editingCategory ? 'Cập nhật' : 'Lưu'}</Button></Space>
            </Form.Item>
        </Form>
    </Modal>
);

export default CategoryModal;
