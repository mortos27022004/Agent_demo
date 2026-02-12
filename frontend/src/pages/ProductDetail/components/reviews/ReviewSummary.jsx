import React from 'react';
import { Typography, Rate, Divider, Progress } from 'antd';

const { Title, Text } = Typography;

const ReviewSummary = ({ avgRating, reviewsCount, ratingCounts }) => (
    <div style={{ height: '100%' }}>
        <div style={{ textAlign: 'center', padding: '16px' }}>
            <Title level={2} style={{ margin: 0, color: '#faad14' }}>{avgRating}/5</Title>
            <Rate disabled allowHalf value={parseFloat(avgRating)} />
            <div style={{ marginTop: 8 }}><Text type="secondary">{reviewsCount} nhận xét</Text></div>
        </div>
        <Divider />
        <div style={{ padding: '0 16px' }}>
            {ratingCounts.map(item => (
                <div key={item.star} style={{ display: 'flex', alignItems: 'center', marginBottom: 8 }}>
                    <Text style={{ width: 60 }}>{item.star} sao</Text>
                    <Progress percent={item.percent} showInfo={false} strokeColor="#faad14" style={{ flex: 1, margin: '0 12px' }} />
                    <Text type="secondary" style={{ width: 30 }}>{item.count}</Text>
                </div>
            ))}
        </div>
    </div>
);

export default ReviewSummary;
