import { Card, Badge } from 'antd';
import { useNavigate } from 'react-router-dom';
import { COLORS } from '../../theme/colors';
import { useCart } from '../../context/CartContext';
import ProductCardMedia from './ProductCardMedia';
import ProductCardContent from './ProductCardContent';
import './ProductCard.css';

const ProductCard = ({ product }) => {
    const navigate = useNavigate();
    const { addToCart } = useCart();
    const { id, name, priceOriginal, priceSale, discountPercent, rating, specs, image } = product;
    const formatPrice = (p) => new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(p);

    const card = (
        <Card hoverable onClick={() => navigate(`/product/${id}`)} className="product-card"
            cover={<ProductCardMedia name={name} image={image} />}>
            <ProductCardContent name={name} specs={specs} priceOriginal={priceOriginal} priceSale={priceSale} rating={rating} formatPrice={formatPrice} />
        </Card>
    );

    return discountPercent > 0 ? (
        <Badge.Ribbon text={`-${discountPercent}%`} color={COLORS.PRIMARY} className="discount-badge">{card}</Badge.Ribbon>
    ) : card;
};

export default ProductCard;
