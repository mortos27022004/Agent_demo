import React from 'react';
import { Row, Col, Form, Input, Typography, Button, Radio, Space, Divider } from 'antd';

const { Title } = Typography;

const CheckoutForms = ({ currentStep, setCurrentStep, form, loading }) => {
    return (
        <>
            {currentStep === 0 && (
                <div className="step-content">
                    <Title level={4}>Thông tin giao hàng</Title>
                    <Row gutter={16}>
                        <Col span={12}>
                            <Form.Item label="Họ tên người nhận" name="recipient" rules={[{ required: true, message: 'Vui lòng nhập họ tên' }]}>
                                <Input placeholder="Ví dụ: Nguyễn Văn A" />
                            </Form.Item>
                        </Col>
                        <Col span={12}>
                            <Form.Item label="Số điện thoại" name="phone" rules={[{ required: true, message: 'Vui lòng nhập số điện thoại' }]}>
                                <Input placeholder="Ví dụ: 0987654321" />
                            </Form.Item>
                        </Col>
                    </Row>
                    <Form.Item label="Địa chỉ chi tiết" name="address" rules={[{ required: true, message: 'Vui lòng nhập địa chỉ giao hàng' }]}>
                        <Input.TextArea rows={3} placeholder="Số nhà, tên đường, phường/xã, quận/huyện..." />
                    </Form.Item>
                    <Form.Item label="Ghi chú (tùy chọn)" name="notes">
                        <Input.TextArea rows={2} placeholder="Lưu ý cho người giao hàng..." />
                    </Form.Item>
                    <Button type="primary" onClick={() => form.validateFields(['recipient', 'phone', 'address']).then(() => setCurrentStep(1))} size="large">Tiếp tục</Button>
                </div>
            )}

            {currentStep === 1 && (
                <div className="step-content">
                    <Title level={4}>Phương thức thanh toán</Title>
                    <Form.Item name="payment_method">
                        <Radio.Group style={{ width: '100%' }}>
                            <Space direction="vertical" style={{ width: '100%' }}>
                                <Radio.Button value="cod" style={{ width: '100%', height: 'auto', padding: '12px' }}>
                                    <div style={{ fontSize: '16px', fontWeight: 'bold' }}>Thanh toán khi nhận hàng (COD)</div>
                                </Radio.Button>
                            </Space>
                        </Radio.Group>
                    </Form.Item>
                    <Divider />
                    <Space>
                        <Button onClick={() => setCurrentStep(0)} size="large">Quay lại</Button>
                        <Button type="primary" htmlType="submit" size="large" loading={loading}>Xác nhận đặt hàng</Button>
                    </Space>
                </div>
            )}
        </>
    );
};

export default CheckoutForms;
