import React from 'react';
import { EyeOutlined, ShoppingCartOutlined } from '@ant-design/icons';

const ProductCardMedia = ({ name, image }) => (
    <div className="product-image-wrapper">
        <img alt={name} src={image} className="product-image" />
    </div>
);

export default ProductCardMedia;
