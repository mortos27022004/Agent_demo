import React from 'react';
import MainLayout from '../../components/layout/MainLayout';
import ProductGrid from '../../components/product/ProductGrid';
import Hero from './components/Hero';

const Home = () => {
    return (
        <MainLayout showSidebar={true}>
            <Hero />
            <div style={{ marginTop: '40px' }}>
                <ProductGrid />
            </div>
        </MainLayout>
    );
};

export default Home;
