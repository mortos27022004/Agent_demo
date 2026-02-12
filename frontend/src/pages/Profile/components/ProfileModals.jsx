import React from 'react';
import { Modal, Form, Input, Button, Select } from 'antd';

const { Option } = Select;

export const EditProfileModal = ({ open, onCancel, form, onFinish }) => (
    <Modal title="Chỉnh sửa thông tin" open={open} onCancel={onCancel} footer={null}>
        <Form form={form} layout="vertical" onFinish={onFinish}>
            <Form.Item name="full_name" label="Họ và tên" rules={[{ required: true }]}><Input /></Form.Item>
            <Form.Item name="phone" label="Số điện thoại"><Input /></Form.Item>
            <Form.Item name="gender" label="Giới tính">
                <Select>
                    <Option value="male">Nam</Option>
                    <Option value="female">Nữ</Option>
                    <Option value="other">Khác</Option>
                </Select>
            </Form.Item>
            <Button type="primary" htmlType="submit" block>Cập nhật</Button>
        </Form>
    </Modal>
);

export const AddAddressModal = ({ open, onCancel, form, onFinish }) => (
    <Modal title="Thêm địa chỉ mới" open={open} onCancel={onCancel} footer={null}>
        <Form form={form} layout="vertical" onFinish={onFinish}>
            <Form.Item name="recipient" label="Tên người nhận" rules={[{ required: true }]}><Input /></Form.Item>
            <Form.Item name="phone" label="Số điện thoại" rules={[{ required: true }]}><Input /></Form.Item>
            <Form.Item name="line1" label="Địa chỉ chi tiết" rules={[{ required: true }]}><Input.TextArea rows={3} /></Form.Item>
            <Button type="primary" htmlType="submit" block>Lưu địa chỉ</Button>
        </Form>
    </Modal>
);
