import React from 'react';
import { Card, Table, Input, InputNumber, Select } from 'antd';

const { Option } = Select;

const VariantTable = ({ variants, onVariantChange }) => {
    if (variants.length === 0) return null;

    const variantColumns = [
        {
            title: 'Tên biến thể',
            dataIndex: 'name',
            key: 'name',
        },
        {
            title: 'SKU',
            dataIndex: 'sku',
            key: 'sku',
            render: (text, record) => (
                <Input
                    value={text}
                    onChange={(e) => onVariantChange(record.key, 'sku', e.target.value)}
                />
            )
        },
        {
            title: 'Giá (đ)',
            dataIndex: 'price',
            key: 'price',
            render: (value, record) => (
                <InputNumber
                    value={value}
                    formatter={value => `${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                    parser={value => value.replace(/\$\s?|(,*)/g, '')}
                    onChange={(val) => onVariantChange(record.key, 'price', val)}
                    style={{ width: '100%' }}
                />
            )
        },
        {
            title: 'Kho',
            dataIndex: 'stock',
            key: 'stock',
            render: (value, record) => (
                <InputNumber
                    value={value}
                    onChange={(val) => onVariantChange(record.key, 'stock', val)}
                    style={{ width: '100%' }}
                />
            )
        },
        {
            title: 'Trạng thái',
            dataIndex: 'status',
            key: 'status',
            width: 140,
            render: (value, record) => (
                <Select
                    value={value || 'active'}
                    onChange={(val) => onVariantChange(record.key, 'status', val)}
                    style={{ width: '100%' }}
                    size="middle"
                >
                    <Option value="active">Đang kinh doanh</Option>
                    <Option value="inactive">Ngừng kinh doanh</Option>
                </Select>
            )
        },
    ];

    return (
        <Card title="Biến thể sản phẩm" style={{ marginBottom: 24, borderRadius: 12 }}>
            <Table
                columns={variantColumns}
                dataSource={variants}
                pagination={false}
                size="middle"
            />
        </Card>
    );
};

export default VariantTable;
