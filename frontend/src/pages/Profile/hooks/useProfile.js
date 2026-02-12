import { useState, useEffect } from 'react';
import { Form, message } from 'antd';
import { useNavigate } from 'react-router-dom';
import userService from '../../../services/user.service';
import authService from '../../../services/auth.service';

export const useProfile = () => {
    const navigate = useNavigate();
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isEditModalOpen, setIsEditModalOpen] = useState(false);
    const [isAddressModalOpen, setIsAddressModalOpen] = useState(false);
    const [form] = Form.useForm();
    const [addressForm] = Form.useForm();

    const fetchProfile = async () => {
        try {
            setLoading(true);
            const res = await userService.getProfile();
            if (res.status === 'success') { setUser(res.data); form.setFieldsValue(res.data); }
        } catch (e) { message.error('Không thể tải thông tin'); } finally { setLoading(false); }
    };

    useEffect(() => { fetchProfile(); }, []);

    const handleUpdateProfile = async (v) => {
        try {
            if ((await userService.updateProfile(v)).status === 'success') {
                message.success('Thành công'); setIsEditModalOpen(false); fetchProfile();
            }
        } catch (e) { message.error('Thất bại'); }
    };

    const handleAddAddress = async (v) => {
        try {
            if ((await userService.addAddress({ ...v, is_default: true })).status === 'success') {
                message.success('Thành công'); setIsAddressModalOpen(false); addressForm.resetFields(); fetchProfile();
            }
        } catch (e) { message.error('Thất bại'); }
    };

    const handleLogout = () => { authService.logout(); navigate('/'); window.location.reload(); };

    return { user, loading, isEditModalOpen, setIsEditModalOpen, isAddressModalOpen, setIsAddressModalOpen, form, addressForm, handleUpdateProfile, handleAddAddress, handleLogout, fetchProfile };
};
