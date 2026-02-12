import React from 'react';
import { Card, Divider, Typography } from 'antd';
import AttributeImageFilter from './AttributeImageFilter';
import AttributeImageValues from './AttributeImageValues';
import ImageManagementArea from './ImageManagementArea';
import AttributeImageSummary from './AttributeImageSummary';

const { Text } = Typography;

const ImageUploadSection = ({ attributes, attributeValues, generalImages, setGeneralImages, selectedImageAttributes, setSelectedImageAttributes, imageAttributeValues, setImageAttributeValues, attributeImages, setAttributeImages, onUploadImage, message }) => {
    const isManagingGeneral = selectedImageAttributes.length === 0;
    const allValuesSelected = selectedImageAttributes.every(attr => imageAttributeValues[attr]);
    const currentAttrKey = !isManagingGeneral && allValuesSelected ? selectedImageAttributes.map(attr => imageAttributeValues[attr]).join('|') : null;
    const currentImages = isManagingGeneral ? generalImages : (currentAttrKey ? (attributeImages[currentAttrKey] || []) : []);

    const handleUpload = async (file) => {
        try {
            const res = await onUploadImage(file);
            if (isManagingGeneral) setGeneralImages(p => [...p, res.url]);
            else setAttributeImages(p => ({ ...p, [currentAttrKey]: [...(p[currentAttrKey] || []), res.url] }));
            message.success(`Đã thêm ảnh: ${file.name}`);
        } catch (e) { message.error(`Lỗi: ${file.name}`); } return false;
    };

    const handleImagesChange = (imgs) => {
        if (isManagingGeneral) setGeneralImages(imgs);
        else if (currentAttrKey) setAttributeImages(p => ({ ...p, [currentAttrKey]: imgs }));
    };

    return (
        <Card title="Hình ảnh sản phẩm" style={{ marginBottom: 24, borderRadius: 12 }}>
            <AttributeImageFilter attrs={attributes.filter(a => a.type === 'option')} selected={selectedImageAttributes} onToggle={(name) => {
                const next = selectedImageAttributes.includes(name) ? selectedImageAttributes.filter(a => a !== name) : [...selectedImageAttributes, name];
                setSelectedImageAttributes(next); if (!next.includes(name)) { const vals = { ...imageAttributeValues }; delete vals[name]; setImageAttributeValues(vals); }
            }} />
            {!isManagingGeneral && <AttributeImageValues selectedAttrs={selectedImageAttributes} attrValues={attributeValues} currentValues={imageAttributeValues} onChange={(n, v) => setImageAttributeValues({ ...imageAttributeValues, [n]: v })} />}
            <Divider />
            {(isManagingGeneral || allValuesSelected) ? <ImageManagementArea isGeneral={isManagingGeneral} images={currentImages} onUpload={handleUpload} onChange={handleImagesChange} /> :
                <div style={{ padding: '40px 20px', textAlign: 'center', background: '#fafafa', borderRadius: '8px', border: '1px dashed #d9d9d9' }}><Text type="secondary">Chọn giá trị cho <b>{selectedImageAttributes.join(', ')}</b> để bắt đầu.</Text></div>}
            {Object.keys(attributeImages).length > 0 && <AttributeImageSummary attributeImages={attributeImages} />}
        </Card>
    );
};

export default ImageUploadSection;
