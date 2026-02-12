Bạn là senior frontend engineer. Hãy tạo frontend trang chủ cho web bán đồ công nghệ (kiểu GearVN) bằng React + Ant Design (antd).

1) Tech stack & yêu cầu chung

React (Vite) + Ant Design.

Chỉ làm frontend UI (không cần API). Dùng mock data để render sản phẩm/danh mục.

Code sạch, tách component rõ ràng, dễ mở rộng.

2) Theme màu (bắt buộc)

Chỉ dùng 3 màu:

Primary: #52c41a (màu chủ đạo)

Black: #0b0b0b

White: #ffffff

Bắt buộc: 2 màu đen và primary phải được lưu trong biến để sau này đổi dễ dàng.

Tạo file src/theme/colors.js:

export const COLORS = { PRIMARY: '#52c41a', BLACK: '#0b0b0b', WHITE: '#ffffff' }

Dùng CSS variables trong src/styles/theme.css:

--color-primary, --color-black, --color-white

Toàn bộ layout dùng các biến này, không hardcode black/white rải rác.

AntD theme:

Set token.colorPrimary = COLORS.PRIMARY

Nền trang chủ chủ yếu white, header black, điểm nhấn bằng #52c41a.

3) Layout trang chủ (giống ảnh)

Tạo trang HomePage gồm 3 phần chính:

A. Top Header (fixed hoặc sticky)

Một thanh header nền black, chữ white, điểm nhấn icon/hover primary.
Bố cục tương tự ảnh:

Logo (text “GEARVN” giả lập) bên trái.

Nút Danh mục (icon menu) mở Dropdown/Drawer danh mục (desktop: dropdown, mobile: drawer).

Search bar ở giữa (AntD Input.Search).

Cụm icon bên phải:

Hotline (1900.5301)

Hệ thống showroom

Tra cứu đơn hàng

Giỏ hàng

Đăng nhập

B. Main content: 2 cột

Left Sidebar (Danh mục) dạng menu dọc giống ảnh:

Laptop

Laptop Gaming

PC GVN

Main, CPU, VGA

Case, Nguồn, Tản

Ổ cứng, RAM, Thẻ nhớ

Loa, Micro, Webcam

Màn hình

Bàn phím

Chuột + Lót chuột

Tai nghe

Ghế - Bàn

Phần mềm, mạng

Handheld, Console

Phụ kiện (Hub, sạc, cáp…)

Dịch vụ và thông tin khác

Sidebar dùng Menu (mode="inline") + icon đơn giản.

Right Content

Một hàng “banner” đơn giản (placeholder) hoặc “Top deals”.

Dưới đó là grid sản phẩm giống ảnh: card sản phẩm có:

Ảnh sản phẩm

Tên sản phẩm (2 dòng, ellipsis)

Dòng specs dạng tag nhỏ (CPU, VGA, RAM, SSD…)

Giá gạch + giá sale màu primary, badge giảm %

Rating (có thể 0.0 như ảnh)

Dùng Row/Col responsive (xl=4 cột, lg=3, md=2, sm=1).

4) Component structure (bắt buộc tách)

Tạo cấu trúc:

src/pages/HomePage.jsx

src/components/layout/AppHeader.jsx

src/components/layout/AppFooter.jsx (footer tối giản)

src/components/sidebar/CategorySidebar.jsx

src/components/product/ProductGrid.jsx

src/components/product/ProductCard.jsx

src/data/mockCategories.js

src/data/mockProducts.js

src/theme/colors.js

src/styles/theme.css

src/styles/layout.css

5) UI/UX yêu cầu

Hover card: viền/box-shadow nhẹ, nút “Xem chi tiết” (optional) xuất hiện khi hover.

Badge giảm giá nằm góc phải trên của card.

Giá sale màu --color-primary. Giá gạch màu xám đậm (nhưng vẫn chỉ dùng 3 màu: xử lý bằng opacity).

Typography rõ ràng, spacing đều.

Mobile: sidebar chuyển sang Drawer khi bấm “Danh mục”.

6) Mock data

mockProducts ít nhất 8–12 sản phẩm. Fields:

id, name, priceOriginal, priceSale, discountPercent, rating, specs: { cpu, gpu, ram, storage }, image

image: dùng placeholder URL hoặc import ảnh local (tối giản).

7) Output yêu cầu

Cung cấp đầy đủ code các file quan trọng để chạy được ngay:

main.jsx, App.jsx, HomePage.jsx, các components, mock data, theme setup.

Kèm hướng dẫn chạy:

npm i

npm run dev

Mục tiêu: Khi chạy sẽ thấy trang chủ giống bố cục ảnh: header + danh mục trái + grid sản phẩm bên phải, màu chủ đạo #52c41a, nền đen/trắng theo biến.