import { Typography, Space, Rate, Divider, Row, Col, Radio, Button, message } from 'antd';
import { ShoppingCartOutlined, ThunderboltOutlined } from '@ant-design/icons';
import { useCart } from '../../../context/CartContext';

const { Title, Text } = Typography;

const ProductInfoSection = ({
    product,
    selectedVariant,
    selectedOptions,
    allOptions,
    handleOptionChange,
    formatPrice
}) => {
    const { addToCart } = useCart();

    const handleAddToCart = () => {
        if (!selectedVariant) {
            message.warning('Vui lòng chọn đầy đủ các tùy chọn sản phẩm');
            return;
        }
        addToCart(product, selectedVariant, 1);
        message.success('Đã thêm sản phẩm vào giỏ hàng');
    };

    return (
        <div className="product-info-card">
            <div className="product-brand">{product.brand_name}</div>
            <Title level={1} className="product-title">{product.name}</Title>

            <Space size="large" style={{ marginBottom: 16 }}>
                <Rate disabled defaultValue={4.5} allowHalf />
                <Text type="secondary">(4.5/5.0 - 128 đánh giá)</Text>
            </Space>

            <div className="product-price-section">
                <span className="detail-price-sale">
                    {formatPrice(selectedVariant?.price || product.variants?.[0]?.price)}
                </span>
                {selectedVariant?.compare_at && (
                    <span className="detail-price-original">
                        {formatPrice(selectedVariant.compare_at)}
                    </span>
                )}
            </div>

            <Divider />

            {/* Options */}
            <div className="variant-selection">
                {Object.entries(allOptions).map(([name, values]) => (
                    <Row key={name} gutter={16} align="middle" className="attribute-group">
                        <Col span={3}>
                            <Text className="attribute-label" style={{ margin: 0 }}>{name}:</Text>
                        </Col>
                        <Col span={20}>
                            <Radio.Group
                                value={selectedOptions[name]}
                                onChange={(e) => handleOptionChange(name, e.target.value)}
                                buttonStyle="solid"
                            >
                                {values.map(val => (
                                    <Radio.Button key={val} value={val}>
                                        {val}
                                    </Radio.Button>
                                ))}
                            </Radio.Group>
                        </Col>
                    </Row>
                ))}
            </div>

            <div className="action-buttons">
                <Button
                    type="primary"
                    size="large"
                    icon={<ShoppingCartOutlined />}
                    className="add-to-cart-btn"
                    onClick={handleAddToCart}
                >
                    Thêm vào giỏ hàng
                </Button>
            </div>
        </div>
    );
};

export default ProductInfoSection;
