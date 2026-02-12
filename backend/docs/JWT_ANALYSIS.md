# Phân Tích Hiện Trạng Xác Thực JWT

Tài liệu này mô tả chi tiết quy trình xác thực JWT hiện tại trong backend, các vấn đề được phát hiện và đề xuất khắc phục.

## 1. Cơ Chế Hoạt Động Hiện Tại (Đã Cài Đặt)

Hệ thống đã có sẵn logic để tạo và xác thực JSON Web Token (JWT).

### Tạo Token

- **File:** `src/services/auth.service.js`
- **Hàm:** `login`
- **Quy trình:**
  1. Xác thực email và mật khẩu của người dùng.
  2. Nếu hợp lệ, tạo JWT sử dụng thư viện `jsonwebtoken`.
  3. **Payload:** Chứa `id` và `email` của người dùng.
  4. **Secret Key:** Sử dụng biến môi trường `JWT_SECRET` (hoặc mặc định `'your_jwt_secret'`).
  5. **Thời hạn:** Token có hiệu lực trong 7 ngày (`7d`).

### Middleware Xác Thực

- **File:** `src/middleware/auth.middleware.js`
- **Middleware:** `protect`
- **Quy trình:**
  1. Kiểm tra header `Authorization` trong request.
  2. Mong đợi định dạng `Bearer <token>`.
  3. Xác thực token bằng secret key.
  4. Nếu hợp lệ, giải mã thông tin user và gán vào `req.user`.
  5. Nếu không hợp lệ hoặc thiếu token, trả về lỗi 401 (Unauthorized).

## 2. Vấn đề Phát Hiện (QUAN TRỌNG)

Mặc dù logic xác thực đã tồn tại, nhưng nó **CHƯA ĐƯỢC ÁP DỤNG** để bảo vệ các route quan trọng.

### Chi tiết

Kiểm tra file `src/routes/category.routes.js`:

```javascript
// const { authenticate, authorize } = require('../middleware/auth.middleware'); // Logic for admin auth
```

- Dòng import middleware đang bị **comment out**.
- Các route nhạy cảm như `POST`, `PUT`, `DELETE` (dùng để tạo, sửa, xóa danh mục) hiện đang **công khai**. Bất kỳ ai cũng có thể gọi API này mà không cần đăng nhập hay có quyền admin.
- Ngoài ra, middleware được export trong `auth.middleware.js` tên là `protect`, nhưng trong route lại đang tham chiếu đến `authenticate` và `authorize`. Điều này sẽ gây lỗi nếu uncomment trực tiếp.

## 3. Đề Xuất Khắc Phục

Cần thực hiện các bước sau để bảo mật hệ thống:

1. **Sửa tên Import:**
    - Trong `category.routes.js` và các file route khác, cập nhật import để sử dụng đúng tên middleware `protect`.

2. **Áp Dụng Middleware:**
    - Thêm middleware `protect` vào trước các route cần bảo vệ (ví dụ: tạo, sửa, xóa dữ liệu).

    *Ví dụ:*

    ```javascript
    const { protect } = require('../middleware/auth.middleware');
    
    router.post('/', protect, categoryController.createCategory);
    router.put('/:id', protect, categoryController.updateCategory);
    router.delete('/:id', protect, categoryController.deleteCategory);
    ```

3. **Bổ Sung Phân Quyền (Authorization - Optional):**
    - Hiện tại `auth.middleware.js` chỉ xác thực đăng nhập (Authentication).
    - Cần thêm middleware `authorize` hoặc kiểm tra `req.user.role` bên trong controller để đảm bảo chỉ Admin mới được thực hiện các thao tác quản lý.
