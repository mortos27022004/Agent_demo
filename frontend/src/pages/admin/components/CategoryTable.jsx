import React from 'react';
import { Table, Button, Space, Tag, Popconfirm } from 'antd';
import { EditOutlined, DeleteOutlined } from '@ant-design/icons';

const CategoryTable = ({ categories, loading, onEdit, onDelete }) => {
    const columns = [
        { title: 'Tên danh mục', dataIndex: 'name', key: 'name', render: (t) => <strong>{t}</strong> },
        { title: 'Slug', dataIndex: 'slug', key: 'slug', render: (t) => <Tag color="blue">{t}</Tag> },
        { title: 'Thuộc tính', dataIndex: 'attributes', key: 'attributes', render: (attrs) => <Space wrap>{attrs?.map(a => <Tag key={a.name} color="cyan">{a.name}</Tag>)}</Space> },
        { title: 'Trạng thái', dataIndex: 'status', key: 'status', render: (s) => <Tag color={s === 'active' ? 'green' : 'orange'}>{(s || 'active').toUpperCase()}</Tag> },
        {
            title: 'Thao tác', key: 'action',
            render: (_, r) => (
                <Space size="middle">
                    <Button type="primary" icon={<EditOutlined />} size="small" onClick={() => onEdit(r)} />
                    <Popconfirm title="Xóa?" onConfirm={() => onDelete(r.id)} okText="Xóa" cancelText="Hủy" okButtonProps={{ danger: true }}>
                        <Button type="primary" danger icon={<DeleteOutlined />} size="small" />
                    </Popconfirm>
                </Space>
            ),
        },
    ];
    return <Table dataSource={categories} columns={columns} rowKey="id" loading={loading} pagination={{ pageSize: 10 }} style={{ background: '#fff', borderRadius: '12px', overflow: 'hidden' }} />;
};

export default CategoryTable;
