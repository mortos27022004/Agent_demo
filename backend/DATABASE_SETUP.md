# Hướng dẫn: Tạo lại Database

Sau khi đã sửa schema, bạn cần tạo lại database với các bước sau:

## Cách 1: Sử dụng công cụ GUI (pgAdmin hoặc DBeaver)

### Bước 1: Drop database cũ (nếu có)

1. Mở pgAdmin hoặc DBeaver
2. Kết nối đến PostgreSQL server
3. Right-click database `ecommerce` → Drop/Delete
4. Xác nhận

### Bước 2: Tạo database mới

1. Right-click "Databases" → Create → Database
2. Tên: `ecommerce`
3. Owner: `postgres`
4. Click Save

### Bước 3: Chạy schema

1. Mở Query Tool trong database `ecommerce`
2. Mở file `create.sql`
3. Copy toàn bộ nội dung
4. Paste vào Query Tool
5. Click Execute (F5)

### Bước 4: Insert dữ liệu mẫu

1. Tiếp tục trong Query Tool
2. Mở file `insert.sql`
3. Copy toàn bộ nội dung  
4. Paste vào Query Tool
5. Click Execute (F5)

## Cách 2: Sử dụng command line (nếu có psql)

```bash
# Bước 1: Drop database cũ
psql -U postgres -c "DROP DATABASE IF EXISTS ecommerce;"

# Bước 2: Tạo database mới
psql -U postgres -c "CREATE DATABASE ecommerce;"

# Bước 3: Chạy schema
psql -U postgres -d ecommerce -f create.sql

# Bước 4: Insert dữ liệu
psql -U postgres -d ecommerce -f insert.sql
```

## Kiểm tra sau khi setup

Chạy query sau để kiểm tra:

```sql
-- Kiểm tra categories
SELECT id, name, slug, icon FROM categories;

-- Kiểm tra products
SELECT id, name, brand_id, is_published FROM products;

-- Kiểm tra variants
SELECT id, sku, variant_name, price, compare_at FROM product_variants;
```

## Restart backend server

Sau khi setup database xong, restart backend server:

```bash
# Ctrl+C để dừng server hiện tại
# Sau đó chạy lại
npm run dev
```
