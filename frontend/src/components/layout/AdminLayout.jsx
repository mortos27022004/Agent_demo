import React, { useState } from 'react';
import { Layout, theme, Breadcrumb } from 'antd';
import { DashboardOutlined, ShoppingOutlined, OrderedListOutlined, UserOutlined, HomeOutlined, FolderOutlined } from '@ant-design/icons';
import { Outlet, useNavigate, useLocation, Link } from 'react-router-dom';
import authService from '../../services/auth.service';
import AdminHeader from './AdminHeader';
import AdminSidebar from './AdminSidebar';

const { Content } = Layout;

const AdminLayout = () => {
    const [collapsed, setCollapsed] = useState(false);
    const navigate = useNavigate();
    const location = useLocation();
    const { token: { colorBgContainer, borderRadiusLG } } = theme.useToken();

    const menuItems = [
        { key: '/', icon: <HomeOutlined />, label: 'Trang chủ' },
        { key: '/admin', icon: <DashboardOutlined />, label: 'Dashboard' },
        {
            key: 'products-group', icon: <FolderOutlined />, label: 'Catalog', children: [
                { key: '/admin/products', label: 'Sản phẩm' },
                { key: '/admin/categories', label: 'Danh mục' }
            ]
        },
        { key: '/admin/orders', icon: <OrderedListOutlined />, label: 'Đơn hàng' },
        { key: '/admin/customers', icon: <UserOutlined />, label: 'Khách hàng' }
    ];

    const pathSnippets = location.pathname.split('/').filter(i => i);
    const breadcrumbItems = [{ title: <Link to="/admin"><HomeOutlined /></Link> }, ...pathSnippets.map((s, i) => ({
        title: i === pathSnippets.length - 1 ? s.charAt(0).toUpperCase() + s.slice(1) : <Link to={`/${pathSnippets.slice(0, i + 1).join('/')}`}>{s.charAt(0).toUpperCase() + s.slice(1)}</Link>
    }))];

    return (
        <Layout style={{ minHeight: '100vh', background: '#F5F7FA' }}>
            <AdminHeader onLogout={() => { authService.logout(); navigate('/'); }} />
            <Layout style={{ marginTop: '64px', background: '#F5F7FA' }}>
                <AdminSidebar collapsed={collapsed} setCollapsed={setCollapsed} menuItems={menuItems} selectedKey={location.pathname} onNavigate={navigate} />
                <Layout style={{ marginLeft: collapsed ? 80 : 200, transition: 'all 0.2s', padding: '0 24px 24px', background: '#F5F7FA' }}>
                    <Breadcrumb items={breadcrumbItems} style={{ margin: '16px 0' }} />
                    <Content style={{ padding: 24, margin: 0, minHeight: 280, background: colorBgContainer, borderRadius: borderRadiusLG, boxShadow: '0 1px 3px rgba(0,0,0,0.02)' }}>
                        <Outlet />
                    </Content>
                </Layout>
            </Layout>
        </Layout>
    );
};

export default AdminLayout;
