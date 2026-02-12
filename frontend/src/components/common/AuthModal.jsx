import React, { useState } from 'react';
import { Modal, Tabs, message } from 'antd';
import { GoogleOutlined, FacebookOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import authService from '../../services/auth.service';
import LoginForm from './auth/LoginForm';
import RegisterForm from './auth/RegisterForm';
import './AuthModal.css';

const AuthModal = ({ open, onCancel }) => {
    const [loading, setLoading] = useState(false);
    const [activeTab, setActiveTab] = useState('1');
    const navigate = useNavigate();

    const handleLogin = async (values) => {
        setLoading(true);
        try {
            const { email, password } = values;
            const res = await authService.login(email, password);
            if (res.status === 'success') {
                message.success('Đăng nhập thành công!');
                onCancel();
                if (res.data.user.role === 'admin') navigate('/admin');
                else window.location.reload();
            }
        } catch (error) {
            message.error(error.response?.data?.message || 'Đăng nhập thất bại!');
        } finally { setLoading(false); }
    };

    const handleSignup = async (values) => {
        setLoading(true);
        try {
            const formattedValues = { ...values, dob: values.dob.format('YYYY-MM-DD') };
            const res = await authService.signup(formattedValues);
            if (res.status === 'success') {
                message.success('Đăng ký thành công! Vui lòng đăng nhập.');
                setActiveTab('1');
            }
        } catch (error) {
            message.error(error.response?.data?.message || 'Đăng ký thất bại!');
        } finally { setLoading(false); }
    };

    const items = [
        { key: '1', label: 'ĐĂNG NHẬP', children: <LoginForm onFinish={handleLogin} loading={loading} /> },
        { key: '2', label: 'ĐĂNG KÝ', children: <RegisterForm onFinish={handleSignup} loading={loading} /> },
    ];

    return (
        <Modal open={open} onCancel={onCancel} footer={null} width={550} className="auth-modal" centered>
            <div className="auth-modal-container">
                <div className="auth-header">
                    <h2>GEARVN</h2>
                    <p>Chào mừng bạn quay trở lại</p>
                </div>
                <div className="auth-body">
                    <Tabs activeKey={activeTab} onChange={setActiveTab} items={items} centered className="auth-tabs" />
                    <div className="auth-footer">
                        <p>Hoặc đăng nhập bằng</p>
                        <div className="social-login">
                            <div className="social-btn"><GoogleOutlined style={{ fontSize: '20px' }} /></div>
                            <div className="social-btn"><FacebookOutlined style={{ fontSize: '20px' }} /></div>
                        </div>
                    </div>
                </div>
            </div>
        </Modal>
    );
};

export default AuthModal;
