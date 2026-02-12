import { useState, useEffect } from 'react';
import { message } from 'antd';
import orderService from '../../../services/order.service';

export const useOrders = () => {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchOrders = async () => {
        try {
            setLoading(true);
            const res = await orderService.getMyOrders();
            if (res.status === 'success') setOrders(res.data);
        } catch (e) {
            console.error('Fetch orders error:', e);
            message.error('Không thể tải danh sách đơn hàng');
        } finally { setLoading(false); }
    };

    useEffect(() => { fetchOrders(); }, []);

    const formatPrice = (p) => new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p || 0);

    return { orders, loading, formatPrice, fetchOrders };
};
