import React from 'react';
import { Card, Space, Typography, Slider, Button, Divider } from 'antd';
import { FilterOutlined } from '@ant-design/icons';

const { Text } = Typography;

const FilterSidebar = ({ priceRange, setPriceRange, setSortBy, formatPrice }) => {
    return (
        <Card title={<Space><FilterOutlined /> Lọc sản phẩm</Space>} style={{ borderRadius: '12px' }}>
            <div style={{ marginBottom: 24 }}>
                <Text strong block style={{ marginBottom: 12 }}>Khoảng giá</Text>
                <Slider
                    range
                    min={0}
                    max={100000000}
                    step={1000000}
                    value={priceRange}
                    onChange={setPriceRange}
                    tipFormatter={(v) => formatPrice(v)}
                />
                <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8 }}>
                    <Text type="secondary" style={{ fontSize: '12px' }}>{formatPrice(priceRange[0])}</Text>
                    <Text type="secondary" style={{ fontSize: '12px' }}>{formatPrice(priceRange[1])}</Text>
                </div>
            </div>
            <Divider />
            <Button
                type="primary"
                block
                onClick={() => {
                    setPriceRange([0, 100000000]);
                    setSortBy('newest');
                }}
            >
                Xóa bộ lọc
            </Button>
        </Card>
    );
};

export default FilterSidebar;
