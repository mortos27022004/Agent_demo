import React from 'react';
import { Divider, Tag } from 'antd';

const AttributeImageSummary = ({ attributeImages }) => (
    <div style={{ marginTop: 32 }}>
        <Divider titlePlacement="left">Danh sách ảnh theo thuộc tính</Divider>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {Object.entries(attributeImages).map(([key, images]) => (
                <Tag key={key} color="blue" style={{ padding: '4px 8px' }}>{key.replace(/\|/g, ' + ')} ({images.length} ảnh)</Tag>
            ))}
        </div>
    </div>
);

export default AttributeImageSummary;
