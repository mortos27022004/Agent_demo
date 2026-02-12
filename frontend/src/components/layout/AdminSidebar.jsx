import React from 'react';
import { Layout, Menu } from 'antd';
import { MenuFoldOutlined, MenuUnfoldOutlined } from '@ant-design/icons';

const { Sider } = Layout;

const AdminSidebar = ({ collapsed, setCollapsed, menuItems, selectedKey, onNavigate }) => (
    <Sider width={200} trigger={null} collapsible collapsed={collapsed} theme="light" style={{ overflow: 'auto', height: 'calc(100vh - 64px)', position: 'fixed', left: 0, top: '64px', bottom: 0, zIndex: 1001, background: '#F5F7FA', borderRight: '1px solid #e8e8e8' }}>
        <Menu theme="light" mode="inline" selectedKeys={[selectedKey]} defaultOpenKeys={['products-group']} items={menuItems} onClick={({ key }) => onNavigate(key)} style={{ height: '100%', borderRight: 0, paddingTop: '16px', background: '#F5F7FA' }} />
        <div onClick={() => setCollapsed(!collapsed)} style={{ position: 'absolute', bottom: 16, left: 0, width: '100%', textAlign: 'center', cursor: 'pointer', color: 'rgba(0,0,0,0.45)' }}>
            {collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
        </div>
    </Sider>
);

export default AdminSidebar;
