import React from 'react';
import { Form, Input, Button, Checkbox } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';

const LoginForm = ({ onFinish, loading }) => {
    return (
        <Form
            name="login_form"
            className="auth-form"
            initialValues={{ remember: true }}
            onFinish={onFinish}
        >
            <Form.Item
                name="email"
                rules={[
                    { required: true, message: 'Vui lòng nhập email!' },
                    { type: 'email', message: 'Email không hợp lệ!' }
                ]}
            >
                <Input
                    prefix={<UserOutlined />}
                    placeholder="Email"
                    size="large"
                    disabled={loading}
                />
            </Form.Item>
            <Form.Item
                name="password"
                rules={[{ required: true, message: 'Vui lòng nhập mật khẩu!' }]}
            >
                <Input.Password
                    prefix={<LockOutlined />}
                    placeholder="Mật khẩu"
                    size="large"
                    disabled={loading}
                />
            </Form.Item>
            <Form.Item>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Form.Item name="remember" valuePropName="checked" noStyle>
                        <Checkbox disabled={loading}>Ghi nhớ</Checkbox>
                    </Form.Item>
                    <a className="login-form-forgot" href="">
                        Quên mật khẩu?
                    </a>
                </div>
            </Form.Item>

            <Form.Item>
                <Button
                    type="primary"
                    htmlType="submit"
                    className="auth-submit-btn"
                    size="large"
                    loading={loading}
                >
                    ĐĂNG NHẬP
                </Button>
            </Form.Item>
        </Form>
    );
};

export default LoginForm;
