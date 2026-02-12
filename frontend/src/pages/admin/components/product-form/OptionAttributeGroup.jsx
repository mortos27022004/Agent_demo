import React from 'react';
import { Row, Col, Form, Input, Radio } from 'antd';
import { DeleteOutlined } from '@ant-design/icons';

const OptionAttributeGroup = ({ attrs, values, inputs, setInputs, onChange }) => (
    <Row gutter={16}>
        {attrs.map((a, i) => (
            <Col xs={24} md={attrs.length % 2 !== 0 && i === attrs.length - 1 ? 24 : 12} key={a.name}>
                <Form.Item label={a.name} required>
                    <div>
                        <Input size="large" placeholder={`Nhập ${a.name} và nhấn Enter`} value={inputs[a.name] || ''} onChange={(e) => setInputs({ ...inputs, [a.name]: e.target.value })} onPressEnter={(e) => {
                            e.preventDefault(); const v = (inputs[a.name] || '').trim();
                            if (v && !(values[a.name] || []).includes(v)) { onChange(a.name, [...(values[a.name] || []), v], 'option'); }
                            setInputs({ ...inputs, [a.name]: '' });
                        }} />
                        <div style={{ marginTop: 8 }}>
                            <Radio.Group optionType="button" size="large" value={null} onChange={(e) => onChange(a.name, (values[a.name] || []).filter(v => v !== e.target.value), 'option')}
                                options={(values[a.name] || []).map(v => ({ label: <span>{v} <DeleteOutlined style={{ marginLeft: 6, color: '#ff4d4f' }} /></span>, value: v }))} />
                        </div>
                    </div>
                </Form.Item>
            </Col>
        ))}
    </Row>
);

export default OptionAttributeGroup;
