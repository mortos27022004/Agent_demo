import React from 'react';
import { Row, Col, Typography } from 'antd';

const { Title, Paragraph } = Typography;

const ProductSpecs = ({ product, selectedOptions }) => {
    return (
        <div className="product-description-section">
            <Row gutter={[40, 40]}>
                <Col xs={24} md={14}>
                    <Title level={3}>Đặc điểm nổi bật</Title>
                    <Paragraph style={{ fontSize: '16px', lineHeight: '1.8' }}>
                        {product.description || 'Chưa có mô tả cho sản phẩm này.'}
                    </Paragraph>
                </Col>
                <Col xs={24} md={10}>
                    <Title level={3}>Thông số kỹ thuật</Title>
                    <div className="specs-grid">
                        {Object.entries(product.specs || {}).map(([key, value]) => (
                            <Row key={key} className="spec-item">
                                <Col span={10}>
                                    <span className="spec-key">{key}</span>
                                </Col>
                                <Col span={14}>
                                    <span className="spec-value">{value}</span>
                                </Col>
                            </Row>
                        ))}
                        {/* Also show selected variant options in specs if they differ */}
                        {Object.entries(selectedOptions).map(([name, value]) => (
                            <Row key={`opt-${name}`} className="spec-item">
                                <Col span={10}>
                                    <span className="spec-key">{name}</span>
                                </Col>
                                <Col span={14}>
                                    <span className="spec-value">{value}</span>
                                </Col>
                            </Row>
                        ))}
                    </div>
                </Col>
            </Row>
        </div>
    );
};

export default ProductSpecs;
