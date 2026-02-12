import React from 'react';
import { Button, Typography } from 'antd';

const { Text } = Typography;

const AttributeImageFilter = ({ attrs, selected, onToggle }) => (
    <div style={{ marginBottom: 24 }}>
        <Text strong style={{ display: 'block', marginBottom: 12 }}>Phân loại theo thuộc tính (Chọn để thêm ảnh riêng, bỏ chọn tất cả để thêm ảnh chung):</Text>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {attrs.map(a => (
                <Button key={a.name} type={selected.includes(a.name) ? 'primary' : 'default'} onClick={() => onToggle(a.name)}>{a.name}</Button>
            ))}
        </div>
    </div>
);

export default AttributeImageFilter;
