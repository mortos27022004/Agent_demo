import React from 'react';
import { Table, Tag, Typography, Button } from 'antd';
import { EyeOutlined } from '@ant-design/icons';
import { COLORS } from '../../../theme/colors';

const { Text } = Typography;

const getStatusTag = (status) => {
    const map = {
        'pending': { color: 'gold', text: 'Chờ xử lý' },
        'paid': { color: 'green', text: 'Đã thanh toán' },
        'shipped': { color: 'blue', text: 'Đang giao hàng' },
        'completed': { color: 'success', text: 'Hoàn thành' },
        'canceled': { color: 'error', text: 'Đã hủy' }
    };
    const c = map[status] || { color: 'default', text: status };
    return <Tag color={c.color}>{c.text.toUpperCase()}</Tag>;
};

const OrderTable = ({ orders, navigate, formatPrice }) => {
    const columns = [
        { title: 'Mã đơn hàng', dataIndex: 'order_code', key: 'order_code', render: (t) => <Text strong>{t}</Text> },
        { title: 'Ngày đặt', dataIndex: 'created_at', key: 'created_at', render: (d) => new Date(d).toLocaleDateString('vi-VN') },
        { title: 'Sản phẩm', key: 'items', render: (_, r) => <Text>{r.items?.length || 0} sản phẩm</Text> },
        { title: 'Tổng cộng', dataIndex: 'total', key: 'total', render: (v) => <Text strong style={{ color: COLORS.PRIMARY }}>{formatPrice(v)}</Text> },
        { title: 'Trạng thái', dataIndex: 'status', key: 'status', render: (s) => getStatusTag(s) },
        { title: 'Hành động', key: 'action', render: (_, r) => <Button type="link" icon={<EyeOutlined />} onClick={() => navigate(`/orders/${r.id}`)}>Chi tiết</Button> }
    ];

    return <Table columns={columns} dataSource={orders} rowKey="id" pagination={{ pageSize: 10 }} />;
};

export default OrderTable;
