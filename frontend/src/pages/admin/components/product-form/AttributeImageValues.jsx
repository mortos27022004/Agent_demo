import React from 'react';
import { Radio, Typography } from 'antd';

const { Text } = Typography;

const AttributeImageValues = ({ selectedAttrs, attrValues, currentValues, onChange }) => (
    <div style={{ marginBottom: 24, display: 'flex', flexWrap: 'wrap', gap: '16px' }}>
        {selectedAttrs.map(name => (
            <span key={name} style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
                <Text>{name}:</Text>
                <Radio.Group value={currentValues[name]} onChange={(e) => onChange(name, e.target.value)} optionType="button" buttonStyle="solid">
                    {(attrValues[name] || []).map(val => <Radio.Button key={val} value={val}>{val}</Radio.Button>)}
                </Radio.Group>
            </span>
        ))}
    </div>
);

export default AttributeImageValues;
