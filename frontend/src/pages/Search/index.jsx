import React from 'react';
import { Row, Col, Typography, Space, Breadcrumb, Select } from 'antd';
import { HomeOutlined } from '@ant-design/icons';
import { Link } from 'react-router-dom';
import MainLayout from '../../components/layout/MainLayout';
import FilterSidebar from './components/FilterSidebar';
import SearchResults from './components/SearchResults';
import { useSearch } from './hooks/useSearch';

const { Title, Text } = Typography;
const { Option } = Select;

const SearchPage = () => {
    const { query, page, products, total, loading, priceRange, setPriceRange, sortBy, setSortBy, handlePageChange } = useSearch();
    const formatPrice = (p) => new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p || 0);

    return (
        <MainLayout>
            <div style={{ padding: '24px', maxWidth: '1400px', margin: '0 auto' }}>
                <Breadcrumb style={{ marginBottom: 24 }} items={[{ title: <Link to="/"><HomeOutlined /> Trang chủ</Link> }, { title: 'Tìm kiếm' }]} />
                <Row gutter={24}>
                    <Col xs={0} lg={6}><FilterSidebar priceRange={priceRange} setPriceRange={setPriceRange} setSortBy={setSortBy} formatPrice={formatPrice} /></Col>
                    <Col xs={24} lg={18}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
                            <div>
                                <Title level={4} style={{ margin: 0 }}>{query ? `Kết quả tìm kiếm cho "${query}"` : 'Tất cả sản phẩm'}</Title>
                                <Text type="secondary">{total} sản phẩm được tìm thấy</Text>
                            </div>
                            <Select defaultValue="newest" value={sortBy} style={{ width: 180 }} onChange={setSortBy}>
                                <Option value="newest">Mới nhất</Option>
                                <Option value="price-asc">Giá tăng dần</Option>
                                <Option value="price-desc">Giá giảm dần</Option>
                            </Select>
                        </div>
                        <SearchResults loading={loading} products={products} total={total} page={page} handlePageChange={handlePageChange} />
                    </Col>
                </Row>
            </div>
        </MainLayout>
    );
};

export default SearchPage;
