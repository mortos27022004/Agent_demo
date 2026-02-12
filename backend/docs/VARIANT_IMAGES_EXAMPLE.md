# Hướng Dẫn Lưu Ảnh Sản Phẩm (Product Images)

Hệ thống hiện tại sử dụng bảng `product_attribute_images` để quản lý toàn bộ hình ảnh của sản phẩm. Cách tiếp cận này cho phép lưu ảnh linh hoạt theo tổ hợp thuộc tính hoặc cho toàn bộ sản phẩm.

## 1. Cấu Trúc Database

Bảng `product_attribute_images` sử dụng cột `attribute_combo` (JSONB) để xác định ảnh thuộc về nhóm nào.

```sql
CREATE TABLE product_attribute_images (
  id               uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  product_id       uuid NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  attribute_combo  jsonb NOT NULL, -- Tổ hợp thuộc tính (ví dụ: {"Màu sắc": "Đỏ"})
  image_urls       text[] NOT NULL, -- Mảng các đường dẫn ảnh
  created_at       timestamptz NOT NULL DEFAULT now()
);
```

- **Ảnh chung toàn sản phẩm**: Đặt `attribute_combo` là một object rỗng `{}`.
- **Ảnh theo thuộc tính cụ thể**: Đặt `attribute_combo` chứa tên và giá trị thuộc tính, ví dụ: `{"Màu sắc": "Đen"}`.

## 2. Quy Trình Lưu Dữ Liệu (Code Example)

### Ví dụ Service Pattern (Node.js)

Dưới đây là cách xử lý trong `product.service.js`:

```javascript
/**
 * Thêm bộ sưu tập ảnh cho sản phẩm
 * @param {string} productId - ID của sản phẩm
 * @param {Object} attributeCombo - Object tổ hợp thuộc tính (dùng {} nếu là ảnh chung)
 * @param {string[]} imageUrls - Mảng các URL của ảnh
 */
const addProductAttributeImages = async (productId, attributeCombo, imageUrls) => {
    const query = `
        INSERT INTO product_attribute_images (product_id, attribute_combo, image_urls)
        VALUES ($1, $2, $3)
        RETURNING *;
    `;
    
    try {
        const result = await db.query(query, [productId, JSON.stringify(attributeCombo), imageUrls]);
        return result.rows[0];
    } catch (error) {
        throw new Error('Không thể lưu ảnh: ' + error.message);
    }
};
```

## 3. Câu Query SQL Kiểm Tra

### Lấy ảnh chung của sản phẩm

```sql
SELECT * FROM product_attribute_images 
WHERE product_id = 'YOUR_PRODUCT_UUID' 
AND attribute_combo = '{}'::jsonb;
```

### Lấy ảnh theo một màu sắc cụ thể

```sql
SELECT * FROM product_attribute_images 
WHERE product_id = 'YOUR_PRODUCT_UUID' 
AND attribute_combo @> '{"Màu sắc": "Đỏ"}'::jsonb;
```

### Lấy tất cả ảnh của một sản phẩm (gồm cả chung và theo thuộc tính)

```sql
SELECT * FROM product_attribute_images 
WHERE product_id = 'YOUR_PRODUCT_UUID';
```
