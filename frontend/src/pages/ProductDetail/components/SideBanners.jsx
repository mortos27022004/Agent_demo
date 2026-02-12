import React from 'react';
import { Col } from 'antd';

export const LeftBanner = () => (
    <Col xs={0} xxl={3} className="side-banner-container">
        <div className="side-banner left-banner">
            <div className="banner-mock-content">ADVERTISEMENT</div>
        </div>
    </Col>
);

export const RightBanner = () => (
    <Col xs={0} xxl={3} className="side-banner-container">
        <div className="side-banner right-banner">
            <div className="banner-mock-content">SPECIAL OFFERS</div>
        </div>
    </Col>
);
