-- Drop existing views
DROP VIEW IF EXISTS inventory_available;

-- Drop existing tables (order matters for CASCADE)
DROP TABLE IF EXISTS product_reviews CASCADE;
DROP TABLE IF EXISTS coupon_redemptions CASCADE;
DROP TABLE IF EXISTS coupons CASCADE;
DROP TABLE IF EXISTS shipments CASCADE;
DROP TABLE IF EXISTS payments CASCADE;
DROP TABLE IF EXISTS order_status_history CASCADE;
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS cart_items CASCADE;
DROP TABLE IF EXISTS carts CASCADE;
DROP TABLE IF EXISTS inventory CASCADE;
DROP TABLE IF EXISTS warehouses CASCADE;
DROP TABLE IF EXISTS product_attribute_images CASCADE;
DROP TABLE IF EXISTS product_variants CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS brands CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS addresses CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS citext;

-- ========== Users & Addresses ==========
CREATE TABLE users (
  id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  email           citext UNIQUE NOT NULL,
  password_hash   text NOT NULL,
  full_name       text,
  phone           text,
  gender          text, -- male/female/other
  date_of_birth   date,
  status          text NOT NULL DEFAULT 'active', -- active/blocked
  role            text NOT NULL DEFAULT 'user',   -- user/admin
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE addresses (
  id            uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id       uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  recipient     text NOT NULL,
  phone         text NOT NULL,
  line1         text NOT NULL,
  line2         text,
  ward          text,
  district      text,
  province      text,
  country       text NOT NULL DEFAULT 'VN',
  is_default    boolean NOT NULL DEFAULT false,
  created_at    timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_addresses_user ON addresses(user_id);

-- ========== Catalog (Simplified Approach) ==========

CREATE TABLE categories (
  id          uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  parent_id   uuid REFERENCES categories(id) ON DELETE SET NULL,
  name        text NOT NULL,
  slug        text UNIQUE NOT NULL,
  icon        text DEFAULT 'info-circle',
  status      text NOT NULL DEFAULT 'active',
  attributes  jsonb DEFAULT '[]'::jsonb
);

CREATE TABLE brands (
  id    uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  name  text UNIQUE NOT NULL,
  slug  text UNIQUE NOT NULL
);

-- Sản phẩm chính (SPU)
CREATE TABLE products (
  id            uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  category_id   uuid REFERENCES categories(id) ON DELETE SET NULL,
  brand_id      uuid REFERENCES brands(id) ON DELETE SET NULL,
  name          text NOT NULL,
  sku           text UNIQUE, -- SKU chung cho sản phẩm (nếu không có variant hoặc là variant default)
  slug          text UNIQUE NOT NULL,
  description   text,
  specs         jsonb DEFAULT '{}'::jsonb,
  is_published  boolean NOT NULL DEFAULT false,
  created_at    timestamptz NOT NULL DEFAULT now(),
  updated_at    timestamptz NOT NULL DEFAULT now()
);

-- Biến thể sản phẩm (SKU)
CREATE TABLE product_variants (
  id             uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  product_id     uuid NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  sku            text UNIQUE NOT NULL,
  variant_name   text,
  attributes     jsonb DEFAULT '{}'::jsonb,
  price          numeric(12,2) NOT NULL CHECK (price >= 0),
  compare_at     numeric(12,2),
  cost           numeric(12,2),
  status         text NOT NULL DEFAULT 'active',
  created_at     timestamptz NOT NULL DEFAULT now(),
  updated_at     timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_variants_product ON product_variants(product_id);
CREATE INDEX idx_products_category ON products(category_id);

-- Ảnh theo tổ hợp thuộc tính (Dùng {} cho ảnh chung toàn sản phẩm)
CREATE TABLE product_attribute_images (
  id               uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  product_id       uuid NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  attribute_combo  jsonb NOT NULL,
  image_urls       text[] NOT NULL,
  created_at       timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_attr_images_product ON product_attribute_images(product_id);

-- ========== Inventory ==========
CREATE TABLE warehouses (
  id        uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  name      text NOT NULL,
  address   text,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE inventory (
  variant_id    uuid NOT NULL REFERENCES product_variants(id) ON DELETE CASCADE, -- trỏ vào biến thể
  warehouse_id  uuid NOT NULL REFERENCES warehouses(id) ON DELETE CASCADE,
  on_hand       int NOT NULL DEFAULT 0 CHECK (on_hand >= 0),
  reserved      int NOT NULL DEFAULT 0 CHECK (reserved >= 0),
  updated_at    timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (variant_id, warehouse_id),
  CHECK (reserved <= on_hand)
);

-- Available stock thường tính: on_hand - reserved
CREATE VIEW inventory_available AS
SELECT variant_id, warehouse_id, (on_hand - reserved) AS available
FROM inventory;

-- ========== Cart ==========
CREATE TABLE carts (
  id          uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id     uuid REFERENCES users(id) ON DELETE SET NULL,
  status      text NOT NULL DEFAULT 'open', -- open/converted/abandoned
  created_at  timestamptz NOT NULL DEFAULT now(),
  updated_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE cart_items (
  cart_id     uuid NOT NULL REFERENCES carts(id) ON DELETE CASCADE,
  variant_id  uuid NOT NULL REFERENCES product_variants(id), -- trỏ vào biến thể
  quantity    int NOT NULL CHECK (quantity > 0),
  PRIMARY KEY (cart_id, variant_id)
);

-- ========== Orders ==========
CREATE TABLE orders (
  id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id         uuid REFERENCES users(id) ON DELETE SET NULL,
  order_code      text UNIQUE NOT NULL, -- mã đơn hiển thị
  status          text NOT NULL DEFAULT 'pending', -- pending/paid/packed/shipped/completed/canceled/refunded
  currency        text NOT NULL DEFAULT 'VND',
  subtotal        numeric(12,2) NOT NULL DEFAULT 0,
  discount_total  numeric(12,2) NOT NULL DEFAULT 0,
  shipping_fee    numeric(12,2) NOT NULL DEFAULT 0,
  total           numeric(12,2) NOT NULL DEFAULT 0,
  shipping_address jsonb NOT NULL DEFAULT '{}'::jsonb, -- snapshot địa chỉ
  customer_notes   text,
  cancel_reason    text,
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE order_status_history (
  id           uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  order_id     uuid NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  status       text NOT NULL,
  comment      text,
  created_at   timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_order_status_history_order ON order_status_history(order_id);

CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);

CREATE TABLE order_items (
  id            uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  order_id      uuid NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  variant_id    uuid REFERENCES product_variants(id) ON DELETE SET NULL, -- trỏ vào biến thể
  sku           text NOT NULL,       -- snapshot
  name          text NOT NULL,       -- snapshot: product name + variant name
  unit_price    numeric(12,2) NOT NULL CHECK (unit_price >= 0),
  quantity      int NOT NULL CHECK (quantity > 0),
  line_total    numeric(12,2) NOT NULL CHECK (line_total >= 0),
  option_details jsonb NOT NULL DEFAULT '[]'::jsonb
);

CREATE INDEX idx_order_items_order ON order_items(order_id);

-- ========== Payments & Shipments ==========
CREATE TABLE payments (
  id           uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  order_id     uuid NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  provider     text NOT NULL,  -- vnpay/momo/stripe/cod...
  amount       numeric(12,2) NOT NULL CHECK (amount >= 0),
  status       text NOT NULL DEFAULT 'initiated', -- initiated/succeeded/failed/refunded
  transaction_ref text,
  raw_payload  jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at   timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_payments_order ON payments(order_id);

CREATE TABLE shipments (
  id           uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  order_id     uuid NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  carrier      text,
  tracking_no  text,
  status       text NOT NULL DEFAULT 'preparing', -- preparing/in_transit/delivered/returned
  shipped_at   timestamptz,
  delivered_at timestamptz,
  created_at   timestamptz NOT NULL DEFAULT now()
);

-- ========== Coupons ==========
CREATE TABLE coupons (
  id           uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  code         text UNIQUE NOT NULL,
  type         text NOT NULL, -- percent/fixed
  value        numeric(12,2) NOT NULL CHECK (value >= 0),
  min_order    numeric(12,2) NOT NULL DEFAULT 0,
  max_uses     int,
  starts_at    timestamptz,
  ends_at      timestamptz,
  is_active    boolean NOT NULL DEFAULT true
);

CREATE TABLE coupon_redemptions (
  coupon_id   uuid NOT NULL REFERENCES coupons(id) ON DELETE CASCADE,
  order_id    uuid NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  user_id     uuid REFERENCES users(id) ON DELETE SET NULL,
  redeemed_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (coupon_id, order_id)
);

-- ========== Reviews ==========
CREATE TABLE product_reviews (
  id          uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  product_id  uuid NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  user_id     uuid REFERENCES users(id) ON DELETE SET NULL,
  order_item_id uuid REFERENCES order_items(id) ON DELETE SET NULL, -- optional: link to specific purchase
  rating      int NOT NULL CHECK (rating >= 1 AND rating <= 5),
  comment     text,
  image_urls  text[],
  created_at  timestamptz NOT NULL DEFAULT now(),
  updated_at  timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_reviews_product ON product_reviews(product_id);
CREATE INDEX idx_reviews_user ON product_reviews(user_id);
