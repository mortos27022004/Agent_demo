-- 1. Thêm các cột vào bảng categories
ALTER TABLE categories 
ADD COLUMN IF NOT EXISTS icon text DEFAULT 'info-circle';

ALTER TABLE categories
ADD COLUMN IF NOT EXISTS status text NOT NULL DEFAULT 'active';

ALTER TABLE categories
ADD COLUMN IF NOT EXISTS attributes jsonb DEFAULT '[]'::jsonb;

-- Cập nhật icon cho categories hiện có
UPDATE categories SET icon = 'laptop' WHERE slug = 'laptop';
UPDATE categories SET icon = 'global' WHERE slug = 'smartphone';

-- Cập nhật status cho categories hiện có
UPDATE categories SET status = 'active' WHERE id IS NOT NULL;

-- Cập nhật attributes mẫu cho categories hiện có
UPDATE categories SET attributes = '[
  {"name":"CPU","type":"text"},
  {"name":"RAM","type":"option"},
  {"name":"Ổ cứng","type":"option"},
  {"name":"Card đồ họa","type":"text"},
  {"name":"Màn hình","type":"text"}
]'::jsonb WHERE slug = 'laptop';

UPDATE categories SET attributes = '[
  {"name":"Chip","type":"text"},
  {"name":"RAM","type":"option"},
  {"name":"Bộ nhớ","type":"option"},
  {"name":"Màn hình","type":"text"},
  {"name":"Màu sắc","type":"option"}
]'::jsonb WHERE slug = 'smartphone';

-- 2. Thêm các cột vào bảng products
ALTER TABLE products
ADD COLUMN IF NOT EXISTS brand_id uuid REFERENCES brands(id) ON DELETE SET NULL;

ALTER TABLE products
ADD COLUMN IF NOT EXISTS specs jsonb DEFAULT '{}'::jsonb;

ALTER TABLE products
ADD COLUMN IF NOT EXISTS is_published boolean NOT NULL DEFAULT false;

-- Cập nhật brand_id cho products hiện có (nếu có data)
-- UPDATE products SET brand_id = 'cccccccc-cccc-cccc-cccc-cccccccccccc' WHERE slug = 'dell-xps-13';
-- UPDATE products SET brand_id = 'dddddddd-dddd-dddd-dddd-dddddddddddd' WHERE slug = 'lenovo-thinkbook-14-g8';
-- UPDATE products SET brand_id = 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee' WHERE slug = 'surface-laptop-studio';

-- Cập nhật is_published cho products hiện có
UPDATE products SET is_published = true WHERE id IS NOT NULL;

-- 3. Thêm các cột vào bảng product_variants
ALTER TABLE product_variants
ADD COLUMN IF NOT EXISTS variant_name text;

ALTER TABLE product_variants
ADD COLUMN IF NOT EXISTS attributes jsonb DEFAULT '{}'::jsonb;

ALTER TABLE product_variants
ADD COLUMN IF NOT EXISTS compare_at numeric(12,2);

ALTER TABLE product_variants
ADD COLUMN IF NOT EXISTS cost numeric(12,2);

-- Cập nhật variant_name cho variants hiện có (nếu có data)
-- UPDATE product_variants SET variant_name = 'Core i7 / 16GB / 512GB' WHERE sku = 'XPS13-I7-16GB-512';
-- UPDATE product_variants SET variant_name = 'Core i5 / 16GB / 512GB' WHERE sku = 'TB14G8-I5-16GB-512';
-- UPDATE product_variants SET variant_name = 'Core i7 / 16GB / 512GB' WHERE sku = 'SLST-I7-16GB-512';

-- =====================================================
-- KIỂM TRA KẾT QUẢ
-- =====================================================

-- Kiểm tra categories
SELECT id, name, slug, icon FROM categories;

-- Kiểm tra products
SELECT 
    id, 
    name, 
    brand_id, 
    is_published,
    specs
FROM products;

-- Kiểm tra product_variants
SELECT 
    id,
    sku,
    variant_name,
    price,
    compare_at,
    cost,
    attributes
FROM product_variants;
