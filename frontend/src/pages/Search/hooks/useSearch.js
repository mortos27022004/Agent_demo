import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import productService from '../../../services/product.service';

export const useSearch = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const query = searchParams.get('q') || '';
    const categoryId = searchParams.get('category_id');
    const page = parseInt(searchParams.get('page') || '1');

    const [products, setProducts] = useState([]);
    const [total, setTotal] = useState(0);
    const [loading, setLoading] = useState(true);
    const [priceRange, setPriceRange] = useState([0, 100000000]);
    const [sortBy, setSortBy] = useState('newest');

    useEffect(() => {
        const fetchResults = async () => {
            try {
                setLoading(true);
                const params = { search: query, page, limit: 12, minPrice: priceRange[0], maxPrice: priceRange[1], published: true };
                if (categoryId) params.category_id = categoryId;
                const response = await productService.getAllProducts(params);
                let sorted = response.products;
                if (sortBy === 'price-asc') sorted.sort((a, b) => a.variants[0]?.price - b.variants[0]?.price);
                else if (sortBy === 'price-desc') sorted.sort((a, b) => b.variants[0]?.price - a.variants[0]?.price);

                setProducts(sorted);
                setTotal(response.pagination.total);
            } catch (err) { console.error('Search error:', err); } finally { setLoading(false); }
        };
        fetchResults();
    }, [query, categoryId, page, priceRange, sortBy]);

    const handlePageChange = (np) => {
        searchParams.set('page', np);
        setSearchParams(searchParams);
        window.scrollTo(0, 0);
    };

    return { query, page, products, total, loading, priceRange, setPriceRange, sortBy, setSortBy, handlePageChange };
};
