import React from 'react';
import { Table, Button, Space, Tag } from 'antd';
import { EditOutlined, DeleteOutlined } from '@ant-design/icons';

const ProductTable = ({ products, loading, navigate }) => {
    const columns = [
        { title: 'Tên sản phẩm', dataIndex: 'name', key: 'name', width: '30%' },
        { title: 'SKU', dataIndex: 'sku', key: 'sku' },
        { title: 'Danh mục', dataIndex: 'category_name', key: 'category_name' },
        {
            title: 'Giá (đ)', key: 'price',
            render: (_, r) => {
                const prices = (r.variants || []).map(v => parseFloat(v.price)).filter(p => !isNaN(p));
                return prices.length > 0 ? Math.min(...prices).toLocaleString() : 'Liên hệ';
            },
            sorter: (a, b) => {
                const getP = (r) => {
                    const ps = (r.variants || []).map(v => parseFloat(v.price)).filter(p => !isNaN(p));
                    return ps.length > 0 ? Math.min(...ps) : 0;
                };
                return getP(a) - getP(b);
            },
        },
        {
            title: 'Trạng thái', dataIndex: 'is_published', key: 'status',
            render: (pub) => <Tag color={pub ? 'green' : 'orange'}>{pub ? 'ĐANG BÁN' : 'BẢN NHÁP'}</Tag>,
        },
        {
            title: 'Thao tác', key: 'action',
            render: (_, r) => (
                <Space size="middle">
                    <Button type="primary" icon={<EditOutlined />} size="small" onClick={() => navigate(`/admin/products/edit/${r.id}`)} />
                    <Button type="primary" danger icon={<DeleteOutlined />} size="small" />
                </Space>
            ),
        },
    ];

    return (
        <Table
            dataSource={products}
            columns={columns}
            rowKey="id"
            loading={loading}
            pagination={{ pageSize: 10 }}
            style={{ background: '#fff', borderRadius: '12px', overflow: 'hidden' }}
        />
    );
};

export default ProductTable;
