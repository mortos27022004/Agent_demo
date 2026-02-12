# Products API Documentation

## Base URL

```
http://localhost:5000/api/v1
```

## Endpoints

### 1. Get All Products

**GET** `/products`

Lấy danh sách tất cả sản phẩm với pagination và filters.

#### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | number | 1 | Số trang |
| `limit` | number | 20 | Số sản phẩm mỗi trang |
| `search` | string | - | Tìm kiếm theo tên sản phẩm |
| `category_id` | uuid | - | Lọc theo danh mục |
| `brand_id` | uuid | - | Lọc theo thương hiệu |
| `published` | boolean | - | Lọc sản phẩm đã publish |

#### Example Request

```bash
# Get all products (page 1, 20 items)
GET http://localhost:5000/api/v1/products

# Get products with pagination
GET http://localhost:5000/api/v1/products?page=2&limit=10

# Search products
GET http://localhost:5000/api/v1/products?search=laptop

# Filter by category and brand
GET http://localhost:5000/api/v1/products?category_id=xxx&brand_id=yyy

# Get only published products
GET http://localhost:5000/api/v1/products?published=true
```

#### Response

```json
{
  "status": "success",
  "message": "Products retrieved successfully",
  "data": {
    "products": [
      {
        "id": "uuid",
        "name": "Product Name",
        "slug": "product-slug",
        "description": "Product description",
        "is_published": true,
        "created_at": "2026-02-06T05:00:00.000Z",
        "category_name": "Category Name",
        "brand_name": "Brand Name",
        "variants": [
          {
            "id": "uuid",
            "sku": "SKU-001",
            "variant_name": "Variant Name",
            "price": "999.00",
            "compare_at": "1299.00",
            "status": "active",
            "attributes": {
              "color": "Black",
              "ram": "16GB"
            }
          }
        ],
        "images": [
          {
            "url": "https://example.com/image.jpg",
            "position": 0
          }
        ]
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100,
      "totalPages": 5
    }
  }
}
```

---

### 2. Get Product by ID

**GET** `/products/:id`

Lấy thông tin chi tiết của một sản phẩm.

#### URL Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | uuid | Product ID |

#### Example Request

```bash
GET http://localhost:5000/api/v1/products/550e8400-e29b-41d4-a716-446655440000
```

#### Response

```json
{
  "status": "success",
  "message": "Product retrieved successfully",
  "data": {
    "id": "uuid",
    "name": "Product Name",
    "slug": "product-slug",
    "description": "Detailed product description",
    "specs": {
      "cpu": "Intel Core i5",
      "ram": "16GB",
      "storage": "512GB SSD"
    },
    "is_published": true,
    "created_at": "2026-02-06T05:00:00.000Z",
    "updated_at": "2026-02-06T05:00:00.000Z",
    "category_id": "uuid",
    "category_name": "Laptops",
    "brand_id": "uuid",
    "brand_name": "Dell",
    "variants": [
      {
        "id": "uuid",
        "sku": "DELL-LAP-001",
        "variant_name": "i5/16GB/512GB - Silver",
        "price": "25000000.00",
        "compare_at": "30000000.00",
        "cost": "20000000.00",
        "status": "active",
        "attributes": {
          "cpu": "i5",
          "ram": "16GB",
          "ssd": "512GB",
          "color": "Silver"
        }
      }
    ],
    "images": [
      {
        "id": "uuid",
        "url": "https://example.com/product-image.jpg",
        "position": 0,
        "variant_id": null
      }
    ]
  }
}
```

#### Error Response (404)

```json
{
  "status": "error",
  "message": "Product not found"
}
```

---

## Testing với cURL

```bash
# Test get all products
curl http://localhost:5000/api/v1/products

# Test with pagination
curl "http://localhost:5000/api/v1/products?page=1&limit=5"

# Test search
curl "http://localhost:5000/api/v1/products?search=laptop"

# Test get product by ID (replace with actual UUID)
curl http://localhost:5000/api/v1/products/YOUR-PRODUCT-UUID
```

---

## File Structure

```
backend/src/
├── controllers/
│   └── product.controller.js    # Request handlers
├── services/
│   └── product.service.js       # Business logic & DB queries
├── routes/
│   └── product.routes.js        # Route definitions
└── app.js                       # Route registration
```

---

## Features Implemented

✅ Pagination (page, limit)  
✅ Search by product name  
✅ Filter by category  
✅ Filter by brand  
✅ Filter by published status  
✅ Get product with variants  
✅ Get product with images  
✅ Get product by ID with full details  
✅ Proper error handling  
✅ Consistent response format  

---

## Next Steps

- [ ] Add authentication middleware
- [ ] Add product creation/update/delete endpoints
- [ ] Add sorting options
- [ ] Add more advanced filters
- [ ] Add cache layer
- [ ] Add API rate limiting
