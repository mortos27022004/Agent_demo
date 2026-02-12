import React, { useState, useEffect } from 'react';
import { Select, InputNumber, Space, Typography, Card, Divider } from 'antd';
import { SortAscendingOutlined, FilterOutlined, TagsOutlined, AppstoreOutlined } from '@ant-design/icons';
import categoryService from '../../services/category.service';
import brandService from '../../services/brand.service';

const { Text } = Typography;
const { Option } = Select;

const ProductFilters = ({ onFilterChange }) => {
    const [categories, setCategories] = useState([]);
    const [brands, setBrands] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState(null);
    const [dynamicAttributes, setDynamicAttributes] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [cats, brs] = await Promise.all([
                    categoryService.getAllCategories(),
                    brandService.getAllBrands()
                ]);
                setCategories(cats);
                setBrands(brs);
            } catch (error) {
                console.error('Error fetching filter data:', error);
            }
        };
        fetchData();
    }, []);

    const handleCategoryChange = (value) => {
        const cat = categories.find(c => c.id === value);
        setSelectedCategory(cat);
        // Extract option-type attributes
        if (cat && cat.attributes) {
            const attrs = Array.isArray(cat.attributes) ? cat.attributes : JSON.parse(cat.attributes || '[]');
            setDynamicAttributes(attrs.filter(a => a.type === 'option'));
        } else {
            setDynamicAttributes([]);
        }
        onFilterChange({ category_id: value });
    };

    const handleBrandChange = (value) => {
        onFilterChange({ brand_id: value });
    };

    const handleDynamicAttrChange = (attrName, value) => {
        onFilterChange({ [`attr_${attrName}`]: value });
    };

    const handleSortChange = (value) => {
        onFilterChange({ sort: value });
    };

    const handlePriceChange = (type, value) => {
        onFilterChange({ [type]: value });
    };

    return (
        <Card className="product-filters-card" style={{ marginBottom: 20, borderRadius: 8 }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
                    <Space size="large" wrap>
                        <Space>
                            <AppstoreOutlined style={{ color: '#8c8c8c' }} />
                            <Text strong>Danh mục:</Text>
                            <Select
                                placeholder="Tất cả danh mục"
                                style={{ width: 180 }}
                                onChange={handleCategoryChange}
                                allowClear
                            >
                                {categories.map(cat => (
                                    <Option key={cat.id} value={cat.id}>{cat.name}</Option>
                                ))}
                            </Select>
                        </Space>

                        <Space>
                            <TagsOutlined style={{ color: '#8c8c8c' }} />
                            <Text strong>Hãng:</Text>
                            <Select
                                placeholder="Tất cả hãng"
                                style={{ width: 150 }}
                                onChange={handleBrandChange}
                                allowClear
                            >
                                {brands.map(brand => (
                                    <Option key={brand.id} value={brand.id}>{brand.name}</Option>
                                ))}
                            </Select>
                        </Space>

                        <Space>
                            <SortAscendingOutlined style={{ color: '#8c8c8c' }} />
                            <Text strong>Sắp xếp:</Text>
                            <Select
                                defaultValue="newest"
                                style={{ width: 180 }}
                                onChange={handleSortChange}
                            >
                                <Option value="newest">Mới nhất</Option>
                                <Option value="price_asc">Giá: Thấp đến Cao</Option>
                                <Option value="price_desc">Giá: Cao đến Thấp</Option>
                                <Option value="rating_desc">Đánh giá cao nhất</Option>
                            </Select>
                        </Space>
                    </Space>

                    <Space>
                        <FilterOutlined style={{ color: '#8c8c8c' }} />
                        <Text strong>Khoảng giá:</Text>
                        <InputNumber
                            placeholder="Từ"
                            min={0}
                            style={{ width: 110 }}
                            onChange={(v) => handlePriceChange('minPrice', v)}
                            formatter={value => `${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                            parser={value => value.replace(/\$\s?|(,*)/g, '')}
                        />
                        <Text type="secondary">-</Text>
                        <InputNumber
                            placeholder="Đến"
                            min={0}
                            style={{ width: 110 }}
                            onChange={(v) => handlePriceChange('maxPrice', v)}
                            formatter={value => `${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                            parser={value => value.replace(/\$\s?|(,*)/g, '')}
                        />
                        <Text type="secondary">₫</Text>
                    </Space>
                </div>

                {dynamicAttributes.length > 0 && (
                    <>
                        <Divider style={{ margin: '8px 0' }} />
                        <Space wrap size="large">
                            <Text strong type="secondary">Bộ lọc chi tiết:</Text>
                            {dynamicAttributes.map(attr => (
                                <Space key={attr.name}>
                                    <Text>{attr.name}:</Text>
                                    <Select
                                        placeholder={`Tất cả ${attr.name}`}
                                        style={{ minWidth: 120 }}
                                        onChange={(v) => handleDynamicAttrChange(attr.name, v)}
                                        allowClear
                                    >
                                        {/* Since backend attributes don't strictly define options, 
                                            we might need to fetch unique values or the user needs to provide them. 
                                            For now, let's assume they are stored in the database if available. 
                                            Actually, let's mock some common options or just show the select.
                                         */}
                                        {/* In a real app, you'd fetch distinct values for this attribute from products of this category */}
                                        <Option value="High">Cao</Option>
                                        <Option value="Medium">Trung bình</Option>
                                        <Option value="Low">Thấp</Option>
                                    </Select>
                                </Space>
                            ))}
                        </Space>
                    </>
                )}
            </div>
        </Card>
    );
};

export default ProductFilters;
