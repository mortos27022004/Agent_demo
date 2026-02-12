import React from 'react';
import { Layout, Badge, Space, Avatar, Typography, Button } from 'antd';
import { BellOutlined, QuestionCircleOutlined, UserOutlined, LogoutOutlined } from '@ant-design/icons';
import { COLORS } from '../../theme/colors';

const { Header } = Layout;
const { Title, Text } = Typography;

const AdminHeader = ({ onLogout }) => (
    <Header style={{ position: 'fixed', zIndex: 1002, width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 24px', background: COLORS.BLACK, boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15)', height: '64px' }}>
        <div style={{ display: 'flex', alignItems: 'center' }}>
            <Title level={4} style={{ margin: 0, color: COLORS.PRIMARY, fontWeight: 'bold', letterSpacing: '2px' }}>GEARVN ADMIN</Title>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
            <Space size="large" style={{ color: COLORS.WHITE, fontSize: '18px' }}>
                <Badge count={5} size="small" offset={[2, 2]}><BellOutlined style={{ cursor: 'pointer', color: COLORS.WHITE }} /></Badge>
                <QuestionCircleOutlined style={{ cursor: 'pointer', color: COLORS.WHITE }} />
            </Space>
            <div style={{ width: '1px', height: '24px', background: 'rgba(255,255,255,0.2)' }} />
            <Space size="middle">
                <Avatar style={{ backgroundColor: COLORS.PRIMARY }} icon={<UserOutlined />} />
                <div style={{ display: 'flex', flexDirection: 'column', lineHeight: '1.2' }}><Text style={{ color: COLORS.WHITE, fontSize: '12px', opacity: 0.8 }}>Admin</Text><Text style={{ color: COLORS.WHITE, fontWeight: 'bold' }}>Manager</Text></div>
                <Button type="text" icon={<LogoutOutlined />} onClick={onLogout} style={{ color: COLORS.WHITE, opacity: 0.7 }}>Thoát</Button>
            </Space>
        </div>
    </Header>
);

export default AdminHeader;
