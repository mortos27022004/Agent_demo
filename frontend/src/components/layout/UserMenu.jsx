import React from 'react';
import { Dropdown } from 'antd';
import { UserOutlined, DashboardOutlined, FileTextOutlined, LogoutOutlined } from '@ant-design/icons';
import { COLORS } from '../../theme/colors';

const UserMenu = ({ user, navigate, handleLogout }) => {
    if (!user) return null;

    const items = [
        ...(user.role === 'admin' ? [{
            key: 'admin',
            label: 'Quản trị hệ thống',
            icon: <DashboardOutlined />,
            onClick: () => navigate('/admin'),
        }] : []),
        {
            key: 'profile',
            label: 'Thông tin tài khoản',
            icon: <UserOutlined />,
            onClick: () => navigate('/profile'),
        },
        {
            key: 'orders',
            label: 'Đơn hàng của tôi',
            icon: <FileTextOutlined />,
            onClick: () => navigate('/orders'),
        },
        { type: 'divider' },
        {
            key: 'logout',
            label: 'Đăng xuất',
            icon: <LogoutOutlined />,
            danger: true,
            onClick: handleLogout,
        },
    ];

    return (
        <Dropdown menu={{ items }} placement="bottomRight" arrow>
            <div className="action-item" style={{ cursor: 'pointer' }}>
                <UserOutlined className="action-icon" style={{ color: COLORS.PRIMARY }} />
                <div className="action-text">
                    <span className="action-label">Chào,</span>
                    <span className="action-value">{user.fullName}</span>
                </div>
            </div>
        </Dropdown>
    );
};

export default UserMenu;
