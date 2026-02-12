import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Divider, message, Form } from 'antd';
import reviewService from '../../../services/review.service';
import authService from '../../../services/auth.service';
import ReviewSummary from './reviews/ReviewSummary';
import ReviewForm from './reviews/ReviewForm';
import ReviewList from './reviews/ReviewList';

const ProductReviews = ({ productId }) => {
    const [reviews, setReviews] = useState([]);
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [form] = Form.useForm();
    const user = authService.getCurrentUser();

    useEffect(() => { fetchReviews(); }, [productId]);

    const fetchReviews = async () => {
        try { setLoading(true); const res = await reviewService.getProductReviews(productId); if (res.status === 'success') setReviews(res.data); }
        catch (e) { console.error(e); } finally { setLoading(false); }
    };

    const avgRating = reviews.length ? (reviews.reduce((s, r) => s + r.rating, 0) / reviews.length).toFixed(1) : 0;
    const ratingCounts = [5, 4, 3, 2, 1].map(s => ({ star: s, count: reviews.filter(r => r.rating === s).length, percent: reviews.length ? (reviews.filter(r => r.rating === s).length / reviews.length) * 100 : 0 }));

    const onFinish = async (v) => {
        try { setSubmitting(true); if ((await reviewService.addReview({ productId, ...v })).status === 'success') { message.success('Cám ơn bạn!'); form.resetFields(); fetchReviews(); } }
        catch (e) { message.error(e.response?.data?.message || 'Lỗi'); } finally { setSubmitting(false); }
    };

    return (
        <Card id="reviews" style={{ marginTop: 24, borderRadius: '12px' }}>
            <Row gutter={[32, 32]}>
                <Col xs={24} md={8}><ReviewSummary avgRating={avgRating} reviewsCount={reviews.length} ratingCounts={ratingCounts} /></Col>
                <Col xs={24} md={16}><ReviewForm user={user} form={form} onFinish={onFinish} submitting={submitting} /></Col>
            </Row>
            <Divider />
            <ReviewList reviews={reviews} loading={loading} />
        </Card>
    );
};

export default ProductReviews;
