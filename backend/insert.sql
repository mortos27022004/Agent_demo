-- ========== USERS ==========
INSERT INTO users (id, email, password_hash, full_name, phone)
VALUES
  ('11111111-1111-1111-1111-111111111111', 'alice@example.com', 'hash_pw_alice', 'Alice Nguyen', '0901000001'),
  ('22222222-2222-2222-2222-222222222222', 'bob@example.com',   'hash_pw_bob',   'Bob Tran',   '0901000002');

-- ========== ADDRESSES ==========
INSERT INTO addresses (
  id, user_id, recipient, phone, line1, district, province, country, is_default
)
VALUES
  (
    uuid_generate_v4(),
    '11111111-1111-1111-1111-111111111111',
    'Alice Nguyen',
    '0901000001',
    '12 Nguyen Hue',
    'District 1',
    'HCM',
    'VN',
    true
  ),
  (
    uuid_generate_v4(),
    '22222222-2222-2222-2222-222222222222',
    'Bob Tran',
    '0901000002',
    '88 Le Loi',
    'Hai Chau',
    'Da Nang',
    'VN',
    true
  );

-- ========== CATEGORIES ==========
INSERT INTO categories (id, parent_id, name, slug, icon, status, attributes)
VALUES
  ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', NULL, 'Laptop', 'laptop', 'laptop', 'active', 
   '[
     {"name":"CPU","type":"text"},
     {"name":"RAM","type":"option"},
     {"name":"Ổ cứng","type":"option"},
     {"name":"Card đồ họa","type":"text"},
     {"name":"Màn hình","type":"text"}
   ]'::jsonb),
  ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', NULL, 'Smartphone', 'smartphone', 'global', 'active',
   '[
     {"name":"Chip","type":"text"},
     {"name":"RAM","type":"option"},
     {"name":"Bộ nhớ","type":"option"},
     {"name":"Màn hình","type":"text"},
     {"name":"Màu sắc","type":"option"}
   ]'::jsonb);

-- ========== BRANDS ==========
INSERT INTO brands (id, name, slug)
VALUES
  ('cccccccc-cccc-cccc-cccc-cccccccccccc', 'Dell', 'dell'),
  ('dddddddd-dddd-dddd-dddd-dddddddddddd', 'Lenovo', 'lenovo'),
  ('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', 'Microsoft', 'microsoft'),
  ('ffffffff-ffff-ffff-ffff-ffffffffffff', 'Apple', 'apple');

-- ========== PRODUCTS (SPU) ==========
-- fixed UUID ids
-- Dell XPS 13           : 0d5a3f4a-7b50-4c66-8aab-1f2f8e0c2a11
-- Lenovo ThinkBook 14 G8: 2b9f6e1d-2f0a-4c9a-a5b2-3c1d6e7f8a22
-- Surface Laptop Studio : 9c6a2b1f-1d3e-4a5b-9c8d-7e6f5a4b3c33
INSERT INTO products (
  id, category_id, brand_id, name, slug, description, specs, is_published
)
VALUES
(
  '0d5a3f4a-7b50-4c66-8aab-1f2f8e0c2a11',
  'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
  'cccccccc-cccc-cccc-cccc-cccccccccccc',
  'Dell XPS 13',
  'dell-xps-13',
  'Ultrabook cao cấp cho lập trình viên',
  '{"screen":"13.4","weight":"1.2kg"}',
  true
),
(
  '2b9f6e1d-2f0a-4c9a-a5b2-3c1d6e7f8a22',
  'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
  'dddddddd-dddd-dddd-dddd-dddddddddddd',
  'Lenovo ThinkBook 14 G8',
  'lenovo-thinkbook-14-g8',
  'Laptop văn phòng mỏng nhẹ',
  '{"screen":"14","weight":"1.4kg"}',
  true
),
(
  '9c6a2b1f-1d3e-4a5b-9c8d-7e6f5a4b3c33',
  'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
  'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee',
  'Surface Laptop Studio',
  'surface-laptop-studio',
  'Laptop lai tablet cao cấp',
  '{"screen":"14.4","touch":true}',
  true
);

-- ========== PRODUCT VARIANTS (SKU) ==========
-- fixed UUID ids
-- Dell variant   : 4a7b1c2d-9e0f-4b3a-8c6d-1f2e3d4c5b6a
-- Lenovo variant : 5b8c2d3e-0f1a-4c2b-9d7e-2a3b4c5d6e7f
-- Surface variant: 6c9d3e4f-1a2b-4d3c-ae8f-3b4c5d6e7f80
INSERT INTO product_variants (
  id, product_id, sku, variant_name, attributes, price, compare_at, cost, status
)
VALUES
(
  '4a7b1c2d-9e0f-4b3a-8c6d-1f2e3d4c5b6a',
  '0d5a3f4a-7b50-4c66-8aab-1f2f8e0c2a11',
  'XPS13-I7-16GB-512',
  'Core i7 / 16GB / 512GB',
  '{"cpu":"i7","ram":"16GB","ssd":"512GB"}',
  42000000,
  45000000,
  38000000,
  'active'
),
(
  '5b8c2d3e-0f1a-4c2b-9d7e-2a3b4c5d6e7f',
  '2b9f6e1d-2f0a-4c9a-a5b2-3c1d6e7f8a22',
  'TB14G8-I5-16GB-512',
  'Core i5 / 16GB / 512GB',
  '{"cpu":"i5","ram":"16GB","ssd":"512GB"}',
  26000000,
  28000000,
  23000000,
  'active'
),
(
  '6c9d3e4f-1a2b-4d3c-ae8f-3b4c5d6e7f80',
  '9c6a2b1f-1d3e-4a5b-9c8d-7e6f5a4b3c33',
  'SLST-I7-16GB-512',
  'Core i7 / 16GB / 512GB',
  '{"cpu":"i7","ram":"16GB","ssd":"512GB"}',
  52000000,
  NULL,
  47000000,
  'active'
);

-- ========== PRODUCT IMAGES (Consolidated to product_attribute_images) ==========
-- Using attribute_combo = '{}' for general images
INSERT INTO product_attribute_images (id, product_id, attribute_combo, image_urls)
VALUES
(
  uuid_generate_v4(),
  '0d5a3f4a-7b50-4c66-8aab-1f2f8e0c2a11',
  '{"cpu":"i7","ram":"16GB","ssd":"512GB"}'::jsonb,
  ARRAY['/static/products/laptop_Dell_Latitude_1724915222125.jpg']
),
(
  uuid_generate_v4(),
  '2b9f6e1d-2f0a-4c9a-a5b2-3c1d6e7f8a22',
  '{"cpu":"i5","ram":"16GB","ssd":"512GB"}'::jsonb,
  ARRAY['/static/products/52877_laptop_lenovo_thinkbook_14_g8_in_21s007mva_5_.jpg']
),
(
  uuid_generate_v4(),
  '9c6a2b1f-1d3e-4a5b-9c8d-7e6f5a4b3c33',
  '{"cpu":"i7","ram":"16GB","ssd":"512GB"}'::jsonb,
  ARRAY['/static/products/Surface-laptop-Studio-avt.png']
),
-- Example of a general image (no specific attribute)
(
  uuid_generate_v4(),
  '0d5a3f4a-7b50-4c66-8aab-1f2f8e0c2a11',
  '{}'::jsonb,
  ARRAY['/static/products/laptop_Dell_Latitude_1724915222125.jpg']
);

-- ========== WAREHOUSES ==========
-- fixed UUID id: 7d2a1b3c-4e5f-4a6b-8c9d-0e1f2a3b4c5d
INSERT INTO warehouses (id, name, address)
VALUES
(
  '7d2a1b3c-4e5f-4a6b-8c9d-0e1f2a3b4c5d',
  'Kho chính HCM',
  'Tan Binh, Ho Chi Minh'
);

-- ========== INVENTORY ==========
INSERT INTO inventory (
  variant_id, warehouse_id, on_hand, reserved
)
VALUES
  ('4a7b1c2d-9e0f-4b3a-8c6d-1f2e3d4c5b6a', '7d2a1b3c-4e5f-4a6b-8c9d-0e1f2a3b4c5d', 10, 2),
  ('5b8c2d3e-0f1a-4c2b-9d7e-2a3b4c5d6e7f', '7d2a1b3c-4e5f-4a6b-8c9d-0e1f2a3b4c5d', 20, 3),
  ('6c9d3e4f-1a2b-4d3c-ae8f-3b4c5d6e7f80', '7d2a1b3c-4e5f-4a6b-8c9d-0e1f2a3b4c5d',  5, 1);

-- ========== CART ==========
-- fixed UUID id: 8a1b2c3d-4e5f-4a6b-9c8d-1e2f3a4b5c6d
INSERT INTO carts (id, user_id, status)
VALUES
(
  '8a1b2c3d-4e5f-4a6b-9c8d-1e2f3a4b5c6d',
  '11111111-1111-1111-1111-111111111111',
  'open'
);

INSERT INTO cart_items (cart_id, variant_id, quantity)
VALUES
(
  '8a1b2c3d-4e5f-4a6b-9c8d-1e2f3a4b5c6d',
  '4a7b1c2d-9e0f-4b3a-8c6d-1f2e3d4c5b6a',
  1
);

-- ========== ORDERS ==========
-- fixed UUID id: 9b2c3d4e-5f6a-4b7c-8d9e-2f3a4b5c6d7e
INSERT INTO orders (
  id, user_id, order_code, status, subtotal, discount_total,
  shipping_fee, total, shipping_address
)
VALUES
(
  '9b2c3d4e-5f6a-4b7c-8d9e-2f3a4b5c6d7e',
  '11111111-1111-1111-1111-111111111111',
  'ORD0001',
  'paid',
  42000000,
  0,
  30000,
  42030000,
  '{"recipient":"Alice Nguyen","address":"12 Nguyen Hue, District 1, HCM"}'
);

-- ========== ORDER ITEMS ==========
INSERT INTO order_items (
  id, order_id, variant_id, sku, name,
  unit_price, quantity, line_total, attributes
)
VALUES
(
  uuid_generate_v4(),
  '9b2c3d4e-5f6a-4b7c-8d9e-2f3a4b5c6d7e',
  '4a7b1c2d-9e0f-4b3a-8c6d-1f2e3d4c5b6a',
  'XPS13-I7-16GB-512',
  'Dell XPS 13 - Core i7 / 16GB / 512GB',
  42000000,
  1,
  42000000,
  '{"cpu":"i7","ram":"16GB","ssd":"512GB"}'
);

-- ========== PAYMENTS ==========
INSERT INTO payments (
  id, order_id, provider, amount, status, transaction_ref, raw_payload
)
VALUES
(
  uuid_generate_v4(),
  '9b2c3d4e-5f6a-4b7c-8d9e-2f3a4b5c6d7e',
  'vnpay',
  42030000,
  'succeeded',
  'VNPAY-DEMO-0001',
  '{"bank":"VCB"}'
);

-- ========== SHIPMENTS ==========
INSERT INTO shipments (
  id, order_id, carrier, tracking_no, status
)
VALUES
(
  uuid_generate_v4(),
  '9b2c3d4e-5f6a-4b7c-8d9e-2f3a4b5c6d7e',
  'GHN',
  'GHN123456789',
  'in_transit'
);
