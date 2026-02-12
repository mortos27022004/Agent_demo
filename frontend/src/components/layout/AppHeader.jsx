import { useState, useEffect } from 'react';
import { Input, Drawer, Button, message } from 'antd';
import { useNavigate } from 'react-router-dom';
import { MenuOutlined } from '@ant-design/icons';
import { COLORS } from '../../theme/colors';
import CategorySidebar from '../sidebar/CategorySidebar';
import AuthModal from '../common/AuthModal';
import authService from '../../services/auth.service';
import { useCart } from '../../context/CartContext';
import HeaderActions from './HeaderActions';
import './AppHeader.css';

const { Search } = Input;

const AppHeader = () => {
    const [drawerVisible, setDrawerVisible] = useState(false);
    const [authModalVisible, setAuthModalVisible] = useState(false);
    const [user, setUser] = useState(authService.getCurrentUser());
    const navigate = useNavigate();
    const { cartCount } = useCart();

    useEffect(() => {
        const handleStorageChange = () => setUser(authService.getCurrentUser());
        window.addEventListener('storage', handleStorageChange);
        return () => window.removeEventListener('storage', handleStorageChange);
    }, []);

    const onSearch = (v) => v.trim() && navigate(`/search?q=${encodeURIComponent(v.trim())}`);

    const handleLogout = () => {
        authService.logout();
        setUser(null);
        message.success('Đã đăng xuất thành công!');
    };

    return (
        <header className="app-header" style={{ backgroundColor: COLORS.BLACK }}>
            <div className="header-container">
                <div className="header-left">
                    <div className="logo" onClick={() => navigate('/')} style={{ cursor: 'pointer' }}>GEARVN</div>
                    <Button className="category-btn" icon={<MenuOutlined />} onClick={() => setDrawerVisible(true)}>Danh mục</Button>
                </div>
                <div className="header-center">
                    <Search placeholder="Bạn cần tìm gì?" onSearch={onSearch} className="search-bar" size="large" enterButton />
                </div>
                <HeaderActions
                    user={user}
                    cartCount={cartCount}
                    navigate={navigate}
                    showAuthModal={() => setAuthModalVisible(true)}
                    handleLogout={handleLogout}
                />
            </div>
            <Drawer title="Danh mục sản phẩm" placement="left" onClose={() => setDrawerVisible(false)} open={drawerVisible}>
                <CategorySidebar mode="inline" />
            </Drawer>
            <AuthModal open={authModalVisible} onCancel={() => setAuthModalVisible(false)} />
        </header>
    );
};

export default AppHeader;
