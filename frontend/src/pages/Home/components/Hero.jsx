import React from 'react';
import { Button, Typography } from 'antd';
import { ShoppingOutlined, RightOutlined } from '@ant-design/icons';
import './Hero.css';

const { Title, Paragraph } = Typography;

const Hero = () => {
    return (
        <div className="hero-section">
            <div className="hero-content">
                <div className="hero-badge">CHƯƠNG TRÌNH KHUYẾN MÃI TẾT 2026</div>
                <Title className="hero-main-title">
                    NÂNG TẦM
                    <br />
                    <span className="highlight">TRẢI NGHIỆM</span>
                </Title>
                <Paragraph className="hero-description">
                    Khám phá bộ sưu tập Gaming Gear và Laptop đời mới nhất.
                    Ưu đãi lên đến 50% cho tất cả các đơn hàng trong tuần lễ này.
                </Paragraph>
                <div className="hero-actions">
                    <Button type="primary" size="large" icon={<ShoppingOutlined />} className="hero-btn-primary">
                        Mua sắm ngay
                    </Button>
                    <Button type="default" size="large" icon={<RightOutlined />} className="hero-btn-secondary">
                        Xem chi tiết
                    </Button>
                </div>
            </div>
            <div className="hero-visual">
                <div className="hero-blob"></div>
                <div className="hero-image-mock">
                    {/* In a real app, this would be a high-quality product image */}
                    <img src="https://gearvn.com/cdn/shop/files/pc_gaming_premium.png" alt="PC Gaming" style={{ width: '100%', height: 'auto' }} />
                </div>
            </div>
        </div>
    );
};

export default Hero;
