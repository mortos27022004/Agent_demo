import React from 'react';
import { Badge } from 'antd';
import { PhoneOutlined, ShopOutlined, FileTextOutlined, ShoppingCartOutlined, UserOutlined } from '@ant-design/icons';
import { COLORS } from '../../theme/colors';
import UserMenu from './UserMenu';

const HeaderActions = ({ user, cartCount, navigate, showAuthModal, handleLogout }) => {
    return (
        <div className="header-right">
            <div className="action-item">
                <PhoneOutlined className="action-icon" />
                <div className="action-text">
                    <span className="action-label">Hotline</span>
                    <span className="action-value">1900.5301</span>
                </div>
            </div>

            <div className="action-item">
                <ShopOutlined className="action-icon" />
                <div className="action-text">
                    <span className="action-label">Hệ thống</span>
                    <span className="action-value">Showroom</span>
                </div>
            </div>

            <div className="action-item" onClick={() => navigate('/orders')} style={{ cursor: 'pointer' }}>
                <FileTextOutlined className="action-icon" />
                <div className="action-text">
                    <span className="action-label">Tra cứu</span>
                    <span className="action-value">Đơn hàng</span>
                </div>
            </div>

            <div className="action-item" onClick={() => navigate('/cart')} style={{ cursor: 'pointer' }}>
                <Badge count={cartCount} showZero style={{ backgroundColor: COLORS.PRIMARY }}>
                    <ShoppingCartOutlined className="action-icon" />
                </Badge>
                <div className="action-text">
                    <span className="action-value">Giỏ hàng</span>
                </div>
            </div>

            {user ? (
                <UserMenu user={user} navigate={navigate} handleLogout={handleLogout} />
            ) : (
                <div className="action-item" onClick={showAuthModal} style={{ cursor: 'pointer' }}>
                    <UserOutlined className="action-icon" />
                    <div className="action-text">
                        <span className="action-value">Đăng nhập</span>
                    </div>
                </div>
            )}
        </div>
    );
};

export default HeaderActions;
