import React from 'react';
import { Card, Divider } from 'antd';
import TextAttributeGroup from './TextAttributeGroup';
import OptionAttributeGroup from './OptionAttributeGroup';

const AttributeManager = ({ selectedCategory, attributes, attributeValues, inputValue, setInputValue, onAttributeValueChange }) => {
    if (!selectedCategory || attributes.length === 0) return null;
    const textAttrs = attributes.filter(a => a.type === 'text');
    const optionAttrs = attributes.filter(a => a.type === 'option');

    return (
        <Card title="Thuộc tính sản phẩm" style={{ marginBottom: 24, borderRadius: 12 }}>
            <Divider titlePlacement="left">Thuộc tính: {selectedCategory.name}</Divider>
            {textAttrs.length > 0 && <TextAttributeGroup attrs={textAttrs} values={attributeValues} onChange={onAttributeValueChange} />}
            {optionAttrs.length > 0 && <OptionAttributeGroup attrs={optionAttrs} values={attributeValues} inputs={inputValue} setInputs={setInputValue} onChange={onAttributeValueChange} />}
        </Card>
    );
};

export default AttributeManager;
