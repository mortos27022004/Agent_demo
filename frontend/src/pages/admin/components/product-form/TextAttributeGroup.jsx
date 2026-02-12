import React from 'react';
import { Row, Col, Form, Input } from 'antd';

const TextAttributeGroup = ({ attrs, values, onChange }) => (
    <Row gutter={16}>
        {attrs.map((a, i) => (
            <Col xs={24} md={attrs.length % 2 !== 0 && i === attrs.length - 1 ? 24 : 12} key={a.name}>
                <Form.Item label={a.name}>
                    <Input size="large" placeholder={`Nhập ${a.name}`} value={values[a.name] || ''} onChange={(e) => onChange(a.name, e.target.value, 'text')} />
                </Form.Item>
            </Col>
        ))}
    </Row>
);

export default TextAttributeGroup;
