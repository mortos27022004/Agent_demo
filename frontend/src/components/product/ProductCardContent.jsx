import React from 'react';
import { Tag, Rate, Card } from 'antd';
import { COLORS } from '../../theme/colors';

const { Meta } = Card;

const ProductCardContent = ({ name, specs, priceOriginal, priceSale, rating, formatPrice }) => {
    const priority = ['color', 'cpu', 'ram', 'storage', 'gpu'];
    const topSpecs = Object.entries(specs || {}).filter(([k, v]) => v && v !== 'N/A')
        .sort((a, b) => (priority.indexOf(a[0]) === -1 ? 999 : priority.indexOf(a[0])) - (priority.indexOf(b[0]) === -1 ? 999 : priority.indexOf(b[0])))
        .slice(0, 4);

    return (
        <Meta title={<div className="product-name" title={name}>{name}</div>} description={
            <div className="product-details">
                <div className="product-specs">{topSpecs.map(([k, v]) => <Tag key={k}>{v}</Tag>)}</div>
                <div className="product-pricing">
                    {priceOriginal > priceSale && <span className="price-original">{formatPrice(priceOriginal)}</span>}
                    <span className="price-sale" style={{ color: COLORS.PRIMARY }}>{formatPrice(priceSale)}</span>
                </div>
                <div className="product-rating"><Rate disabled defaultValue={rating} allowHalf /><span className="rating-value">({rating?.toFixed(1) || '0.0'})</span></div>
            </div>
        } />
    );
};

export default ProductCardContent;
