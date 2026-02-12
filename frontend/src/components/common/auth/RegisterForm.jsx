import React from 'react';
import { Form, Button } from 'antd';
import RegisterFormBasicInfo from './RegisterFormBasicInfo';
import RegisterFormAccountInfo from './RegisterFormAccountInfo';

const RegisterForm = ({ onFinish, loading }) => (
    <Form name="signup_form" className="auth-form" onFinish={onFinish} layout="vertical">
        <RegisterFormBasicInfo loading={loading} />
        <RegisterFormAccountInfo loading={loading} />
        <Form.Item style={{ marginBottom: 0 }}>
            <Button type="primary" htmlType="submit" className="auth-submit-btn" size="large" loading={loading}>ĐĂNG KÝ NGAY</Button>
        </Form.Item>
    </Form>
);

export default RegisterForm;
