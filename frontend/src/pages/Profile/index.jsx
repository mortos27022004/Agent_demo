import React from 'react';
import { Row, Col, Typography, Card, Avatar, Tabs, Divider } from 'antd';
import { UserOutlined, EnvironmentOutlined, LogoutOutlined } from '@ant-design/icons';
import MainLayout from '../../components/layout/MainLayout';
import PersonalInfo from './components/PersonalInfo';
import AddressBook from './components/AddressBook';
import { EditProfileModal, AddAddressModal } from './components/ProfileModals';
import { useProfile } from './hooks/useProfile';

const { Title, Text } = Typography;

const ProfilePage = () => {
    const { user, isEditModalOpen, setIsEditModalOpen, isAddressModalOpen, setIsAddressModalOpen, form, addressForm, handleUpdateProfile, handleAddAddress, handleLogout, fetchProfile } = useProfile();

    const items = [
        { key: '1', label: <span><UserOutlined />Thông tin chung</span>, children: <PersonalInfo user={user} setIsEditModalOpen={setIsEditModalOpen} /> },
        { key: '2', label: <span><EnvironmentOutlined />Sổ địa chỉ</span>, children: <AddressBook addresses={user?.addresses} setIsAddressModalOpen={setIsAddressModalOpen} fetchProfile={fetchProfile} /> }
    ];

    return (
        <MainLayout>
            <div style={{ padding: '24px', maxWidth: '1000px', margin: '0 auto', minHeight: '80vh' }}>
                <Row gutter={24}>
                    <Col xs={24} md={6}>
                        <Card style={{ textAlign: 'center', borderRadius: '12px' }}>
                            <Avatar size={80} icon={<UserOutlined />} src={user?.avatar} />
                            <Title level={4} style={{ marginTop: 16, marginBottom: 4 }}>{user?.full_name}</Title>
                            <Text type="secondary">{user?.email}</Text>
                            <Divider />
                            <Card.Grid hoverable={false} onClick={handleLogout} style={{ width: '100%', textAlign: 'center', cursor: 'pointer', color: '#ff4d4f' }}><LogoutOutlined /> Đăng xuất</Card.Grid>
                        </Card>
                    </Col>
                    <Col xs={24} md={18}><Card style={{ borderRadius: '12px' }} bodyStyle={{ padding: '0 24px 24px' }}><Tabs defaultActiveKey="1" items={items} /></Card></Col>
                </Row>
                <EditProfileModal open={isEditModalOpen} onCancel={() => setIsEditModalOpen(false)} form={form} onFinish={handleUpdateProfile} />
                <AddAddressModal open={isAddressModalOpen} onCancel={() => setIsAddressModalOpen(false)} form={addressForm} onFinish={handleAddAddress} />
            </div>
        </MainLayout>
    );
};

export default ProfilePage;
