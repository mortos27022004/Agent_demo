import { useState } from 'react';
import { message } from 'antd';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../../../context/CartContext';
import orderService from '../../../services/order.service';

export const useCheckoutLogic = () => {
    const navigate = useNavigate();
    const { cartItems, cartTotal, clearCart } = useCart();
    const [currentStep, setCurrentStep] = useState(0);
    const [loading, setLoading] = useState(false);
    const [isSuccess, setIsSuccess] = useState(false);
    const [orderInfo, setOrderInfo] = useState(null);

    const onFinish = async (values) => {
        try {
            setLoading(true);
            const orderData = {
                address: { recipient: values.recipient, phone: values.phone, line1: values.address },
                payment_method: values.payment_method,
                notes: values.notes
            };
            const res = await orderService.createOrder(orderData);
            if (res.status === 'success') {
                setOrderInfo(res.data);
                setIsSuccess(true);
                clearCart();
                message.success('Đặt hàng thành công!');
            }
        } catch (error) {
            message.error(error.response?.data?.message || 'Lỗi khi đặt hàng');
        } finally { setLoading(false); }
    };

    return {
        navigate, cartItems, cartTotal, currentStep, setCurrentStep,
        loading, isSuccess, orderInfo, onFinish
    };
};
