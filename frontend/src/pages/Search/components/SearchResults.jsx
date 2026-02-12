import React from 'react';
import { Row, Col, Card, Typography, Pagination, Spin } from 'antd';
import ProductCard from '../../../components/product/ProductCard';

const { Text } = Typography;

const SearchResults = ({ loading, products, total, page, handlePageChange }) => {
    if (loading) return <div style={{ textAlign: 'center', padding: '100px' }}><Spin size="large" /></div>;
    if (products.length === 0) return (
        <Card style={{ textAlign: 'center', padding: '64px' }}>
            <Text type="secondary">Không tìm thấy sản phẩm nào khớp với tiêu chí của bạn.</Text>
        </Card>
    );

    return (
        <>
            <Row gutter={[16, 16]}>
                {products.map(product => (
                    <Col xs={12} sm={8} md={8} lg={6} key={product.id}>
                        <ProductCard product={product} />
                    </Col>
                ))}
            </Row>
            <div style={{ textAlign: 'center', marginTop: 48 }}>
                <Pagination
                    current={page}
                    total={total}
                    pageSize={12}
                    onChange={handlePageChange}
                    showSizeChanger={false}
                />
            </div>
        </>
    );
};

export default SearchResults;
