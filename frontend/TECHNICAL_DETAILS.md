# Chi Tiết Kỹ Thuật - Tính Năng Kéo Thả Ảnh

## 📁 Cấu Trúc File

```
frontend/
├── src/
│   ├── components/
│   │   └── common/
│   │       ├── DraggableImageGallery.jsx      (NEW)
│   │       └── DraggableImageGallery.css      (NEW)
│   └── pages/
│       └── admin/
│           ├── AddProduct.jsx                 (MODIFIED)
│           └── EditProduct.jsx                (MODIFIED)
└── DRAG_DROP_FEATURE_GUIDE.md                 (NEW)
```

## 🔧 Component: DraggableImageGallery

### Props
```javascript
{
  images: string[],           // Mảng các URL ảnh
  onImagesChange: (images) => void,  // Callback khi thay đổi thứ tự
  maxImages?: number          // (Optional) Số lượng ảnh tối đa
}
```

### State Management
```javascript
- draggedIndex: null | number   // Index của ảnh đang được kéo
- hoveredIndex: null | number   // Index của vị trí hover
```

### Event Handlers

#### `handleDragStart(e, index)`
- Được gọi khi bắt đầu kéo ảnh
- Lưu lại index của ảnh đang kéo
- Đặt `dropEffect = 'move'`

#### `handleDragOver(e, index)`
- Được gọi khi kéo ảnh qua một ảnh khác
- Cập nhật `hoveredIndex` để hiển thị vị trí thả

#### `handleDrop(e, dropIndex)`
- Xử lý thả ảnh vào vị trí mới
- Thực hiện sắp xếp lại mảng ảnh:
  1. Xóa ảnh từ vị trí cũ
  2. Chèn ảnh vào vị trí mới
- Gọi `onImagesChange` với mảng mới

#### `handleRemoveImage(index)`
- Xóa ảnh tại index
- Cập nhật state bằng `onImagesChange`

### CSS Classes

#### `.draggable-gallery`
- Grid layout: `grid-template-columns: repeat(auto-fill, minmax(120px, 1fr))`
- Gap: 12px
- Background: #fafafa

#### `.image-item`
- Aspect ratio: 1:1
- Border: 2px solid #d9d9d9
- Transition: 0.3s ease
- States:
  - `:hover` - Viền sáng lên
  - `.dragging` - Opacity 0.5, scale 0.95, viền đỏ
  - `.drag-over` - Viền xanh, scale 1.02, background light

#### `.image-overlay`
- Absolute positioning
- Background: rgba(0, 0, 0, 0.5)
- Hiển thị khi hover

#### `.drag-handle`, `.delete-btn`
- Width/Height: 36px
- Border-radius: 4px
- Cursor: pointer
- Hover effects: scale 1.1

#### `.image-index`
- Vị trí: bottom-right
- Kích thước: 28px (circle)
- Font-size: 12px

## 🔄 Data Flow

### AddProduct.jsx
```
Upload (empty fileList) 
  ↓
productService.uploadImage()
  ↓
setGeneralImages([...prev, result.url])
  ↓
DraggableImageGallery (display + reorder)
  ↓
onSubmit: Lưu mảng generalImages có thứ tự mới
```

### EditProduct.jsx
```
Load Product
  ↓
setGeneralImages(product.attribute_images[0].image_urls)
  ↓
DraggableImageGallery (display + reorder)
  ↓
(Optional) Upload thêm ảnh mới
  ↓
onSubmit: Lưu mảng generalImages có thứ tự mới
```

## 🎯 Luồng Hoạt Động Chi Tiết

### Sắp Xếp Ảnh (Drag & Drop)
1. **Drag Start** → `handleDragStart()`
   - Lưu `draggedIndex`
   - Set `dataTransfer.effectAllowed = 'move'`

2. **Drag Over** → `handleDragOver()`
   - Cập nhật `hoveredIndex`
   - Hiển thị visual feedback (viền xanh)

3. **Drop** → `handleDrop()`
   - Kiểm tra `draggedIndex !== dropIndex`
   - Sắp xếp lại mảng:
     ```javascript
     const newImages = [...images];
     const draggedImage = newImages[draggedIndex];
     newImages.splice(draggedIndex, 1);
     newImages.splice(dropIndex, 0, draggedImage);
     ```
   - Gọi `onImagesChange(newImages)`
   - Reset `draggedIndex` và `hoveredIndex`

4. **Drag End** → `handleDragEnd()`
   - Reset visual states

### Xóa Ảnh
1. Click nút Delete
2. Gọi `handleRemoveImage(index)`
3. Filter ra ảnh cần xóa
4. Gọi `onImagesChange()` với mảng mới

## 📦 Integration Points

### AddProduct.jsx
- Import: Line 7
- Sử dụng: 
  - Ảnh chung: Line 463
  - Ảnh thuộc tính: Line 534

### EditProduct.jsx
- Import: Line 7
- Sử dụng:
  - Ảnh chung: Line 601
  - Ảnh thuộc tính: Line 666

## 🚀 Performance Considerations

- ✅ Không sử dụng `key={index}` (dùng `key={url}`)
- ✅ State updates tối thiểu
- ✅ CSS transitions thay vì animations
- ✅ Cleanup drag state trong `handleDragEnd`

## 🔍 Browser Compatibility

- ✅ Chrome 13+
- ✅ Firefox 3.6+
- ✅ Safari 6+
- ✅ Edge 12+
- ⚠️ IE11 - Partial support (drag-drop works, CSS Grid may need prefix)

## 📝 Testing Checklist

- [ ] Upload một ảnh
- [ ] Kéo thả để sắp xếp
- [ ] Xóa ảnh bằng nút delete
- [ ] Upload thêm ảnh, sắp xếp lại
- [ ] Lưu sản phẩm và kiểm tra thứ tự
- [ ] Chỉnh sửa sản phẩm, sắp xếp lại ảnh
- [ ] Upload ảnh theo thuộc tính và sắp xếp
- [ ] Responsive test trên mobile (nếu áp dụng)
