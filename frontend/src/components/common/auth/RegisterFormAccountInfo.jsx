import React from 'react';
import { Form, Input } from 'antd';
import { LockOutlined } from '@ant-design/icons';

const RegisterFormAccountInfo = ({ loading }) => (
    <div style={{ display: 'flex', gap: '10px' }}>
        <Form.Item name="password" label="Mật khẩu" style={{ flex: 1 }} rules={[{ required: true, message: 'Nhập mật khẩu!' }, { min: 6, message: 'Ít nhất 6 ký tự!' }]}><Input.Password prefix={<LockOutlined />} placeholder="Mật khẩu" size="large" disabled={loading} /></Form.Item>
        <Form.Item name="confirm" label="Xác nhận" style={{ flex: 1 }} dependencies={['password']} rules={[{ required: true, message: 'Xác nhận mật khẩu!' }, ({ getFieldValue }) => ({ validator(_, value) { return !value || getFieldValue('password') === value ? Promise.resolve() : Promise.reject(new Error('Không khớp!')); } })]}><Input.Password prefix={<LockOutlined />} placeholder="Nhập lại" size="large" disabled={loading} /></Form.Item>
    </div>
);

export default RegisterFormAccountInfo;
