import React from 'react';
import { Form, Input, Select, DatePicker } from 'antd';
import { UserOutlined, MailOutlined, PhoneOutlined, HomeOutlined } from '@ant-design/icons';

const { Option } = Select;

const RegisterFormBasicInfo = ({ loading }) => (
    <>
        <Form.Item name="fullName" label="Họ và tên" rules={[{ required: true, message: 'Nhập họ tên!' }]}><Input prefix={<UserOutlined />} placeholder="Nguyễn Văn A" size="large" disabled={loading} /></Form.Item>
        <div style={{ display: 'flex', gap: '10px' }}>
            <Form.Item name="email" label="Email" style={{ flex: 1 }} rules={[{ required: true, message: 'Nhập email!' }, { type: 'email', message: 'Hợp lệ!' }]}><Input prefix={<MailOutlined />} placeholder="email@example.com" size="large" disabled={loading} /></Form.Item>
            <Form.Item name="phone" label="Số điện thoại" style={{ flex: 1 }} rules={[{ required: true, message: 'Nhập số điện thoại!' }]}><Input prefix={<PhoneOutlined />} placeholder="09xx..." size="large" disabled={loading} /></Form.Item>
        </div>
        <Form.Item name="address" label="Địa chỉ" rules={[{ required: true, message: 'Nhập địa chỉ!' }]}><Input prefix={<HomeOutlined />} placeholder="Địa chỉ" size="large" disabled={loading} /></Form.Item>
        <div style={{ display: 'flex', gap: '10px' }}>
            <Form.Item name="gender" label="Giới tính" style={{ flex: 1 }} rules={[{ required: true, message: 'Chọn giới tính!' }]}><Select placeholder="Chọn" size="large" disabled={loading}><Option value="male">Nam</Option><Option value="female">Nữ</Option></Select></Form.Item>
            <Form.Item name="dob" label="Ngày sinh" style={{ flex: 1 }} rules={[{ required: true, message: 'Chọn ngày sinh!' }]}><DatePicker style={{ width: '100%' }} size="large" placeholder="Ngày/Tháng/Năm" format="DD/MM/YYYY" disabled={loading} /></Form.Item>
        </div>
    </>
);

export default RegisterFormBasicInfo;
