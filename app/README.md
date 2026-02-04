# Agno Agent - Streamlit Demo Interface

Giao diện web tương tác để demo và hiển thị đầy đủ quá trình hoạt động của Agno AI Agent.

## 🚀 Khởi động ứng dụng

### 1. Kích hoạt môi trường ảo

```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Chạy Streamlit app

```bash
streamlit run app/streamlit_app.py
```

Ứng dụng sẽ mở tại: <http://localhost:8501>

## ✨ Tính năng

### 💬 Chat Interface

- Giao diện chat tương tác với agent
- Hiển thị lịch sử hội thoại
- Real-time response streaming

### 🔍 Process Visualization

- Hiển thị quá trình suy nghĩ của agent
- Tracking tool calls (calculator, sum_1_to_n)
- Timeline thực thi

### 📋 Session Management

- Xem tất cả sessions trong database
- Chuyển đổi giữa các sessions
- Tạo session mới
- Export lịch sử hội thoại

### ⚙️ Configuration Panel

- Session ID configuration
- Debug mode toggle
- Agent settings

### 📊 Analytics

- Thống kê sessions và messages
- Tool usage tracking
- Response time metrics

## 📁 Cấu trúc

```
app/
├── __init__.py          # Package init
├── streamlit_app.py     # Main Streamlit application
└── streamlit_helper.py  # Helper functions
```

## 🔧 Yêu cầu

- Python 3.11+
- OpenAI API Key (trong file `.env`)
- Các dependencies trong `requirements.txt`

## 💡 Sử dụng

1. Nhấn nút "🔄 Khởi tạo Agent" ở sidebar
2. Đợi agent khởi tạo thành công
3. Nhập câu hỏi vào ô chat
4. Xem agent trả lời và process log ở sidebar
5. Export conversation nếu cần

## 🐛 Debug Mode

Bật Debug Mode ở sidebar để xem:

- Chi tiết cấu hình agent
- Session state
- Thông tin database path
- Tool call details
