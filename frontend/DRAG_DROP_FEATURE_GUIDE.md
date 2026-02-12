# Hướng Dẫn Sử Dụng Tính Năng Kéo Thả Ảnh

## 📋 Tổng Quan Thay Đổi

Đã thêm tính năng kéo thả (drag-and-drop) để sắp xếp thứ tự các ảnh sản phẩm trong phần thêm và chỉnh sửa sản phẩm.

## 🆕 File Mới Được Tạo

### 1. `frontend/src/components/common/DraggableImageGallery.jsx`
- Component React để hiển thị và quản lý ảnh với tính năng kéo thả
- Cho phép người dùng:
  - **Kéo thả** để sắp xếp lại thứ tự ảnh
  - **Xóa** từng ảnh bằng nút delete
  - **Xem** số thứ tự ảnh ở góc dưới phải

### 2. `frontend/src/components/common/DraggableImageGallery.css`
- Stylesheet cho component DraggableImageGallery
- Bao gồm styling cho:
  - **Lưới ảnh** (grid layout)
  - **Hiệu ứng kéo thả** (dragging, drag-over)
  - **Overlay điều khiển** (delete, drag handle)
  - **Chỉ số ảnh**

## ✏️ File Được Chỉnh Sửa

### 1. `frontend/src/pages/admin/AddProduct.jsx`
**Thay đổi:**
- Thêm import `DraggableImageGallery`
- Thay thế Upload component bằng DraggableImageGallery cho:
  - **Ảnh chung sản phẩm** (generalImages)
  - **Ảnh theo thuộc tính** (attributeImages)

### 2. `frontend/src/pages/admin/EditProduct.jsx`
**Thay đổi:**
- Thêm import `DraggableImageGallery`
- Thay thế Upload component bằng DraggableImageGallery cho:
  - **Ảnh chung sản phẩm** (generalImages)
  - **Ảnh theo thuộc tính** (attributeImages)

## 🎨 Tính Năng Chi Tiết

### Drag and Drop
- **Giao diện trực quan**: Khi kéo ảnh, ảnh sẽ mờ đi 50%
- **Thả vào**: Vị trí thả sẽ có viền xanh để hiển thị nơi ảnh sẽ được đặt
- **Số thứ tự**: Hiển thị tự động ở góc dưới phải của mỗi ảnh

### Xóa Ảnh
- Nút xóa xuất hiện khi hover vào ảnh
- Có biểu tượng delete nổi bật

### Hình Ảnh Động
- **Hover effect**: Đường viền sáng lên khi di chuột
- **Dragging effect**: Ảnh đang kéo sẽ mờ và nhỏ lại
- **Drop zone**: Vùng thả có viền xanh và nền sáng

## 🚀 Cách Sử Dụng

### Thêm Sản Phẩm Mới
1. Vào trang "Thêm sản phẩm mới"
2. Tại mục "Hình ảnh sản phẩm"
3. Tải lên ảnh bằng nút "Upload"
4. **Kéo thả các ảnh để sắp xếp thứ tự**
5. Nhấn "Lưu sản phẩm"

### Chỉnh Sửa Sản Phẩm
1. Vào trang "Chỉnh sửa sản phẩm"
2. Tại mục "Hình ảnh sản phẩm"
3. **Kéo thả các ảnh hiện tại để thay đổi thứ tự**
4. Có thể tải lên ảnh mới và sắp xếp
5. Nhấn "Cập nhật sản phẩm"

## 💡 Lợi Ích

✅ **Trải nghiệm người dùng tốt hơn**: Sắp xếp ảnh trực quan và dễ dàng
✅ **Giao diện hiện đại**: Hỗ trợ drag-and-drop chuẩn web
✅ **Quản lý ảnh linh hoạt**: Thay đổi thứ tự bất cứ lúc nào
✅ **Tương thích đầy đủ**: Hoạt động với cả ảnh chung và ảnh theo thuộc tính

## 📝 Lưu Ý

- Thứ tự ảnh được lưu khi nhấn nút "Lưu sản phẩm" hoặc "Cập nhật sản phẩm"
- Có thể sắp xếp lại ảnh nhiều lần trước khi lưu
- Ảnh đầu tiên sẽ là ảnh đại diện sản phẩm
