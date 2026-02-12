# Luồng xử lý API Request trong Backend

## 📊 Sơ đồ tổng quan

```
Frontend (React/Browser)
         │
         ▼
    HTTP Request
    GET /api/v1/products
         │
         ▼
┌────────────────────────────────────────┐
│      Backend (Node.js + Express)       │
│                                        │
│  ① server.js (Entry Point)            │
│         │                              │
│         ▼                              │
│  ② app.js (Express App)               │
│         │                              │
│         ▼                              │
│  ③ Middleware (CORS, JSON parser...)  │
│         │                              │
│         ▼                              │
│  ④ Routes (product.routes.js)         │
│         │                              │
│         ▼                              │
│  ⑤ Controller (product.controller.js) │
│         │                              │
│         ▼                              │
│  ⑥ Service (product.service.js)       │
│         │                              │
│         ▼                              │
│  ⑦ Database (PostgreSQL)              │
│         │                              │
│         ▼                              │
│    Response Data                       │
└────────────────────────────────────────┘
         │
         ▼
    HTTP Response (JSON)
         │
         ▼
Frontend receives data
```

---

## 🔄 Chi tiết từng bước

### ① **server.js** - Entry Point (Điểm khởi đầu)

**File**: [`server.js`](file:///d:/2025%20-%20S2/HTTMDT/E-Web-Project/backend/server.js)

```javascript
require('dotenv').config();        // Load biến môi trường từ .env
const app = require('./src/app'); // Import Express app

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
```

**Nhiệm vụ**:

- ✅ Load environment variables (`.env`)
- ✅ Import Express app
- ✅ Khởi động server và lắng nghe trên port 5000
- ✅ **Chỉ chạy 1 lần** khi start server

---

### ② **app.js** - Express Application Setup

**File**: [`src/app.js`](file:///d:/2025%20-%20S2/HTTMDT/E-Web-Project/backend/src/app.js)

```javascript
const express = require('express');
const cors = require('cors');

const app = express();

// Middleware
app.use(cors());                           // ③ CORS middleware
app.use(express.json());                   // ③ Parse JSON body
app.use(express.urlencoded({ extended: true }));

// Routes
app.use('/api/v1/products', require('./routes/product.routes')); // ④

module.exports = app;
```

**Nhiệm vụ**:

- ✅ Tạo Express application
- ✅ Đăng ký middleware
- ✅ Đăng ký routes
- ✅ Export app để `server.js` sử dụng

---

### ③ **Middleware** - Xử lý trước khi đến route

**Chạy tuần tự theo thứ tự trong `app.js`**:

1. **CORS Middleware** (`cors()`):
   - Cho phép frontend từ domain khác gọi API
   - Thêm headers: `Access-Control-Allow-Origin`, etc.

2. **JSON Parser** (`express.json()`):
   - Parse request body thành JavaScript object
   - VD: `{"name": "Product"}` → `req.body.name`

3. **URL Encoded Parser**:
   - Parse form data

**⚠️ Middleware chạy cho MỌI request**

---

### ④ **Routes** - Route Matching

**File**: [`src/routes/product.routes.js`](file:///d:/2025%20-%20S2/HTTMDT/E-Web-Project/backend/src/routes/product.routes.js)

```javascript
const express = require('express');
const router = express.Router();
const productController = require('../controllers/product.controller');

// GET /api/v1/products
router.get('/', productController.getAllProducts);

// GET /api/v1/products/:id
router.get('/:id', productController.getProductById);

module.exports = router;
```

**Nhiệm vụ**:

- ✅ Định nghĩa các endpoints
- ✅ Map URL → Controller function
- ✅ Xác định HTTP method (GET, POST, PUT, DELETE)

**Ví dụ request matching**:

```
Request: GET /api/v1/products?page=1&limit=10
         └─────┬────┘ └────┬────┘ └────┬──────┘
               │           │            │
         Base path      Route      Query params
         (app.js)    (routes.js)   (controller xử lý)
```

---

### ⑤ **Controller** - Request Handler (Xử lý request)

**File**: [`src/controllers/product.controller.js`](file:///d:/2025%20-%20S2/HTTMDT/E-Web-Project/backend/src/controllers/product.controller.js)

```javascript
const productService = require('../services/product.service');
const { successResponse, errorResponse } = require('../utils/response.util');

const getAllProducts = async (req, res) => {
  try {
    // 1. Lấy parameters từ request
    const { page = 1, limit = 20, search } = req.query;

    // 2. Xây dựng filters
    const filters = {
      limit: parseInt(limit),
      offset: (parseInt(page) - 1) * parseInt(limit),
      search: search
    };

    // 3. Gọi Service layer để lấy data
    const [products, totalCount] = await Promise.all([
      productService.getAllProducts(filters),  // ⑥
      productService.getProductCount(filters)
    ]);

    // 4. Format và trả response
    return successResponse(res, {
      products,
      pagination: { page, limit, total: totalCount }
    });

  } catch (error) {
    // 5. Xử lý lỗi
    return errorResponse(res, error.message, 500);
  }
};
```

**Nhiệm vụ**:

- ✅ Nhận request (`req`) và response object (`res`)
- ✅ Parse và validate request parameters
- ✅ Gọi Service layer để xử lý business logic
- ✅ Format response và trả về client
- ✅ Xử lý errors

**Request Object (`req`) chứa**:

```javascript
req.query      // Query parameters: ?page=1&limit=10
req.params     // URL parameters: /:id
req.body       // Request body (JSON)
req.headers    // HTTP headers
```

---

### ⑥ **Service** - Business Logic Layer

**File**: [`src/services/product.service.js`](file:///d:/2025%20-%20S2/HTTMDT/E-Web-Project/backend/src/services/product.service.js)

```javascript
const db = require('../../config/database');

const getAllProducts = async (filters = {}) => {
  try {
    // 1. Xây dựng SQL query
    let query = `
      SELECT 
        p.id, p.name, p.slug,
        json_agg(pv.*) as variants
      FROM products p
      LEFT JOIN product_variants pv ON p.id = pv.product_id
    `;

    const conditions = [];
    const params = [];

    // 2. Thêm WHERE conditions dựa trên filters
    if (filters.search) {
      conditions.push(`p.name ILIKE $1`);
      params.push(`%${filters.search}%`);
    }

    if (conditions.length > 0) {
      query += ' WHERE ' + conditions.join(' AND ');
    }

    query += ' GROUP BY p.id';

    // 3. Execute query ⑦
    const result = await db.query(query, params);

    // 4. Return data
    return result.rows;

  } catch (error) {
    throw error;
  }
};
```

**Nhiệm vụ**:

- ✅ Xây dựng SQL queries
- ✅ Xử lý business logic
- ✅ Tương tác với database
- ✅ Transform data nếu cần
- ✅ Không quan tâm đến HTTP request/response

---

### ⑦ **Database** - PostgreSQL Connection

**File**: [`config/database.js`](file:///d:/2025%20-%20S2/HTTMDT/E-Web-Project/backend/config/database.js)

```javascript
const { Pool } = require('pg');

const pool = new Pool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: process.env.DB_PORT
});

module.exports = pool;
```

**Nhiệm vụ**:

- ✅ Tạo connection pool đến PostgreSQL
- ✅ Execute SQL queries
- ✅ Return kết quả từ database

**Khi gọi `db.query()`**:

1. Lấy connection từ pool
2. Chạy SQL query
3. Trả về kết quả (rows)
4. Release connection về pool

---

## 📝 Ví dụ cụ thể

### Request từ Frontend

```javascript
// Frontend code (React)
fetch('http://localhost:5000/api/v1/products?page=1&limit=10')
  .then(res => res.json())
  .then(data => console.log(data));
```

### Luồng xử lý trong Backend

```
1️⃣ server.js
   → Server đang chạy, lắng nghe port 5000
   → Nhận request: GET /api/v1/products?page=1&limit=10

2️⃣ app.js
   → Request đi qua middleware stack
   → CORS: ✅ Allow cross-origin
   → JSON Parser: ✅ Ready to parse JSON

3️⃣ Route Matching
   → Tìm route match: /api/v1/products → product.routes.js
   → Method match: GET → router.get('/')
   → Gọi: productController.getAllProducts

4️⃣ Controller (product.controller.js)
   → Nhận req, res
   → Parse query: page=1, limit=10
   → Tạo filters: { limit: 10, offset: 0 }
   → Gọi: productService.getAllProducts(filters)

5️⃣ Service (product.service.js)
   → Nhận filters
   → Build SQL query:
     SELECT p.*, json_agg(pv.*) as variants
     FROM products p
     LEFT JOIN product_variants pv ON p.id = pv.product_id
     GROUP BY p.id
     LIMIT 10 OFFSET 0
   → Gọi: db.query(query)

6️⃣ Database
   → Connection pool lấy connection
   → Execute SQL query trên PostgreSQL
   → Return rows: [{ id: '...', name: 'Laptop', variants: [...] }, ...]

7️⃣ Service returns → Controller
   → Service trả data về Controller
   → products = [...]

8️⃣ Controller format response
   → Tạo response object:
     {
       status: 'success',
       message: 'Products retrieved successfully',
       data: {
         products: [...],
         pagination: { page: 1, limit: 10, total: 50 }
       }
     }
   → res.json(...) → Gửi về Frontend

9️⃣ Frontend nhận response
   → Response: 200 OK
   → Body: { status: 'success', data: {...} }
```

---

## 🎯 Tóm tắt

| Tầng | File | Trách nhiệm | Chạy khi nào |
|------|------|-------------|--------------|
| **Entry** | `server.js` | Start server | 1 lần khi khởi động |
| **App** | `src/app.js` | Setup Express | 1 lần khi khởi động |
| **Middleware** | Built-in | Parse request | Mỗi request |
| **Route** | `src/routes/*.routes.js` | Map URL → Controller | Mỗi request |
| **Controller** | `src/controllers/*.controller.js` | Xử lý request/response | Mỗi request |
| **Service** | `src/services/*.service.js` | Business logic + DB | Khi controller gọi |
| **Database** | `config/database.js` | Query PostgreSQL | Khi service cần data |

---

## 🔑 Nguyên tắc quan trọng

1. **Separation of Concerns** (Tách biệt trách nhiệm):
   - Route: Chỉ định nghĩa endpoints
   - Controller: Xử lý HTTP request/response
   - Service: Business logic và database queries

2. **Request Object Flow**:

   ```
   Route → Controller (req, res) → Service (data only) → Database
   ```

3. **Response Flow**:

   ```
   Database → Service (rows) → Controller (format) → Client (JSON)
   ```

4. **Error Handling**:
   - Service throw error
   - Controller catch và format error response
   - Client nhận error message

---

## 🧪 Debug Tips

Để trace request flow, thêm console.log:

```javascript
// server.js
console.log('✅ Server started');

// app.js - thêm middleware
app.use((req, res, next) => {
  console.log(`📨 ${req.method} ${req.url}`);
  next();
});

// Controller
console.log('🎯 Controller: getAllProducts called');
console.log('📋 Filters:', filters);

// Service
console.log('🔍 Service: Executing query');
console.log('📝 SQL:', query);

// Database result
console.log('💾 DB returned:', result.rows.length, 'rows');
```

Khi chạy sẽ thấy:

```
📨 GET /api/v1/products?page=1
🎯 Controller: getAllProducts called
📋 Filters: { limit: 10, offset: 0 }
🔍 Service: Executing query
📝 SQL: SELECT p.* FROM products...
💾 DB returned: 10 rows
```
