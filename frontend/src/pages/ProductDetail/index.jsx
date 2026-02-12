import React, { useMemo } from 'react';
import { Row, Col, Spin, Breadcrumb } from 'antd';
import { HomeOutlined } from '@ant-design/icons';
import { useParams } from 'react-router-dom';
import MainLayout from '../../components/layout/MainLayout';
import ProductGallery from './components/ProductGallery';
import ProductInfoSection from './components/ProductInfoSection';
import ProductSpecs from './components/ProductSpecs';
import ProductReviews from './components/ProductReviews';
import { useProductDetail } from './hooks/useProductDetail';
import { LeftBanner, RightBanner } from './components/SideBanners';
import './ProductDetailPage.css';

const ProductDetailPage = () => {
    const { id } = useParams();
    const { 
        loading, 
        product, 
        selectedVariant, 
        selectedOptions, 
        activeImageSet, 
        imageIndex, 
        setImageIndex, 
        allOptions, 
        handleOptionChange 
    } = useProductDetail(id);
    const formatPrice = (p) => new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p || 0);

    if (loading) return <MainLayout><div style={{ padding: '100px', textAlign: 'center' }}><Spin size="large" tip="Đang tải..." /></div></MainLayout>;
    if (!product) return null;

    return (
        <MainLayout>
            <div className="product-detail-page-wrapper">
                <Row gutter={[24, 24]} justify="center">
                    <LeftBanner />
                    <Col xs={24} lg={22} xxl={18}>
                        <div className="product-detail-container">
                            <Breadcrumb style={{ marginBottom: 24 }} items={[{ title: <HomeOutlined />, href: '/' }, { title: product.category_name, href: `/category/${product.category_id}` }, { title: product.name }]} />
                            <div className="product-main-content-card">
                                <Row gutter={[40, 40]}>
                                    <Col xs={24} lg={10}>
                                        <ProductGallery 
                                            imageSet={activeImageSet} 
                                            imageIndex={imageIndex} 
                                            setImageIndex={setImageIndex} 
                                            title={product.name} 
                                        />
                                    </Col>
                                    <Col xs={24} lg={14}>
                                        <ProductInfoSection 
                                            product={product} 
                                            selectedVariant={selectedVariant} 
                                            selectedOptions={selectedOptions} 
                                            allOptions={allOptions} 
                                            handleOptionChange={handleOptionChange} 
                                            formatPrice={formatPrice} 
                                        />
                                    </Col>
                                </Row>
                            </div>
                            <ProductSpecs 
                                product={product} 
                                selectedOptions={selectedOptions} 
                            />
                            <ProductReviews productId={product.id} />
                        </div>
                    </Col>
                    <RightBanner />
                </Row>
            </div>
        </MainLayout>
    );
};

export default ProductDetailPage;
