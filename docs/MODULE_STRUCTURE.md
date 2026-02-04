# Cấu Trúc Module - Agno Agent

## 📁 Tổng Quan Cấu Trúc

Dự án đã được tái cấu trúc thành các module riêng biệt để dễ bảo trì và mở rộng:

```
Agent/
├── __init__.py           # Package initialization & exports
├── main.py              # Entry point chính
├── config.py            # Cấu hình agent
├── tools.py             # Tool functions
├── agent_manager.py     # Quản lý agent lifecycle
├── requirements.txt     # Dependencies
├── .env                 # Environment variables
└── README.md           # Documentation
```

## 📄 Chi Tiết Các Module

### 1. **config.py**
**Chức năng**: Quản lý cấu hình cho agent

**Nội dung**:
- `AgentConfig` dataclass chứa tất cả cấu hình
- Properties để truy cập database path và API key
- Các cài đặt mặc định có thể tùy chỉnh

**Sử dụng**:
```python
from config import AgentConfig

config = AgentConfig(
    model_id="gpt-4o-mini",
    debug_mode=True
)
```

---

### 2. **tools.py**
**Chức năng**: Chứa các tool functions cho agent

**Nội dung**:
- `sum_1_to_n(n)`: Tính tổng từ 1 đến n
- `calculator(a, b, operation)`: Máy tính đơn giản

**Sử dụng**:
```python
from tools import sum_1_to_n, calculator

result = sum_1_to_n(10)  # 55
result = calculator(5, 3, "add")  # 8.0
```

---

### 3. **agent_manager.py**
**Chức năng**: Quản lý việc khởi tạo và chạy agent

**Nội dung**:
- `AgnoAgentManager` class
- Methods:
  - `setup_database()`: Khởi tạo database
  - `setup_tracing()`: Bật tracing
  - `create_agent()`: Tạo agent instance
  - `initialize()`: Khởi tạo đầy đủ
  - `run_questions()`: Chạy danh sách câu hỏi

**Sử dụng**:
```python
from config import AgentConfig
from agent_manager import AgnoAgentManager

config = AgentConfig()
manager = AgnoAgentManager(config)
manager.initialize()
manager.run_questions(["Câu hỏi của bạn"])
```

---

### 4. **main.py**
**Chức năng**: Entry point chính của ứng dụng

**Nội dung**:
- Import các module cần thiết
- Cấu hình logging
- Function `main()` để chạy ứng dụng

**Chạy**:
```bash
python main.py
```

---

### 5. **__init__.py**
**Chức năng**: Biến thư mục thành Python package

**Nội dung**:
- Export các class và function chính
- Metadata (version, author)
- `__all__` để định nghĩa public API

## 🎯 Lợi Ích Của Cấu Trúc Mới

### ✅ **Tách Biệt Trách Nhiệm (Separation of Concerns)**
- Mỗi module có một mục đích cụ thể
- Dễ tìm và sửa code

### ✅ **Dễ Bảo Trì (Maintainability)**
- Thay đổi cấu hình không ảnh hưởng đến logic agent
- Thêm tools mới chỉ cần chỉnh sửa `tools.py`

### ✅ **Tái Sử Dụng (Reusability)**
- Có thể import và sử dụng các module trong file khác
- Ví dụ: `from agent_manager import AgnoAgentManager`

### ✅ **Dễ Test (Testability)**
- Mỗi module có thể được test riêng biệt
- Mock dependencies dễ dàng hơn

### ✅ **Scalability**
- Dễ mở rộng thêm tools mới
- Dễ thêm các cấu hình phức tạp hơn

## 🔧 Cách Mở Rộng

### Thêm Tool Mới
Chỉnh sửa `tools.py`:
```python
def new_tool(param: str) -> str:
    """Tool mới của bạn."""
    return f"Result: {param}"
```

Sau đó cập nhật `agent_manager.py`:
```python
from tools import sum_1_to_n, calculator, new_tool

# Trong create_agent():
tools=[
    Function.from_callable(sum_1_to_n),
    Function.from_callable(calculator),
    Function.from_callable(new_tool),  # Thêm tool mới
],
```

### Thay Đổi Cấu Hình
Chỉnh sửa `config.py`:
```python
@dataclass
class AgentConfig:
    model_id: str = "gpt-4o"  # Thay đổi model
    temperature: float = 0.7  # Thêm cấu hình mới
    # ... các cấu hình khác
```

## 📝 Migration từ Code Cũ

**Trước đây**: Tất cả code trong 1 file `main.py` (190 dòng)

**Bây giờ**: Code được chia thành:
- `config.py` (38 dòng)
- `tools.py` (58 dòng)
- `agent_manager.py` (164 dòng)
- `main.py` (62 dòng)
- `__init__.py` (20 dòng)

**Tổng kết**: Code dễ đọc, dễ bảo trì hơn nhiều!

## 🚀 Chạy Ứng Dụng

```bash
# Cách 1: Chạy trực tiếp
python main.py

# Cách 2: Chạy như module
python -m main

# Cách 3: Sử dụng script setup
./setup_and_run.sh
```

## 🧪 Testing

```bash
# Kiểm tra syntax
python -m py_compile config.py tools.py agent_manager.py main.py

# Chạy với debug logging
python main.py
```
