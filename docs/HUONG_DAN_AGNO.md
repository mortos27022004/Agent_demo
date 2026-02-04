# Hướng Dẫn Cài Đặt và Chạy Demo Agno

## Mục Tiêu
Hướng dẫn này giúp bạn cài đặt và chạy một Agent AI đơn giản bằng Agno trên máy local.

---

## 1. Prerequisites (Kiểm Tra Yêu Cầu)

Trước khi bắt đầu, hãy đảm bảo máy bạn có:

- [ ] **Python 3.8 trở lên** (khuyến nghị Python 3.10 hoặc 3.11)
  ```bash
  python --version
  # hoặc
  python3 --version
  ```

- [ ] **Conda** (Anaconda hoặc Miniconda)
  ```bash
  conda --version
  ```
  
  > **Nếu chưa có Conda:** Tải Miniconda tại [docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)

- [ ] **OpenAI API Key** - Đăng ký tại [platform.openai.com](https://platform.openai.com/)

---

## 2. Cài Đặt

### 2.1. Cho Windows (PowerShell)

```powershell
# Bước 1: Tạo thư mục project
mkdir agno-demo
cd agno-demo

# Bước 2: Tạo Conda environment với Python 3.11
conda create -n agno-env python=3.11 -y

# Bước 3: Kích hoạt Conda environment
conda activate agno-env

# Bước 4: Cài đặt Agno
pip install agno

# Bước 5: Set biến môi trường OPENAI_API_KEY (tạm thời - chỉ trong session hiện tại)
$env:OPENAI_API_KEY="sk-your-api-key-here"

# Bước 6: Set biến môi trường vĩnh viễn (cho user hiện tại)
conda env config vars set OPENAI_API_KEY=sk-your-api-key-here -n agno-env

# Sau đó deactivate và activate lại để biến môi trường có hiệu lực
conda deactivate
conda activate agno-env
```

> **Lưu ý**: Biến môi trường được set bằng `conda env config vars` sẽ tự động load mỗi khi activate environment.

---

### 2.2. Cho macOS/Linux

```bash
# Bước 1: Tạo thư mục project
mkdir agno-demo
cd agno-demo

# Bước 2: Tạo Conda environment với Python 3.11
conda create -n agno-env python=3.11 -y

# Bước 3: Kích hoạt Conda environment
conda activate agno-env

# Bước 4: Cài đặt Agno
pip install agno

# Bước 5: Set biến môi trường OPENAI_API_KEY (tạm thời - chỉ trong session hiện tại)
export OPENAI_API_KEY="sk-your-api-key-here"

# Bước 6: Set biến môi trường vĩnh viễn (gắn với conda environment)
conda env config vars set OPENAI_API_KEY=sk-your-api-key-here -n agno-env

# Sau đó deactivate và activate lại để biến môi trường có hiệu lực
conda deactivate
conda activate agno-env

# Kiểm tra biến môi trường đã set chưa
echo $OPENAI_API_KEY
```

---

## 3. Tạo File Demo

Tạo file `main.py` với nội dung sau:

```python
"""
Demo Agno Agent với OpenAI
- Sử dụng model gpt-4o-mini
- Có tool tính tổng để demo agent gọi tool
- Lưu memory vào file JSON
"""

import os
import json
from pathlib import Path
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.memory.db.json import JsonMemoryDb
from agno.tools.function import Function


# ========================================
# 1. Định nghĩa Tool (Hàm Python)
# ========================================
def sum_1_to_n(n: int) -> int:
    """
    Tính tổng các số từ 1 đến n.
    
    Args:
        n: Số nguyên dương
        
    Returns:
        Tổng từ 1 đến n
    """
    if n < 1:
        return 0
    return sum(range(1, n + 1))


def calculator(a: float, b: float, operation: str) -> float:
    """
    Máy tính đơn giản để thực hiện các phép toán cơ bản.
    
    Args:
        a: Số thứ nhất
        b: Số thứ hai
        operation: Phép toán ("add", "subtract", "multiply", "divide")
        
    Returns:
        Kết quả phép tính
    """
    operations = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else float('inf')
    }
    return operations.get(operation, 0)


# ========================================
# 2. Thiết Lập Memory
# ========================================
# Đường dẫn file memory
MEMORY_FILE = Path(__file__).parent / "memory.json"

# Tạo file memory.json nếu chưa tồn tại
if not MEMORY_FILE.exists():
    MEMORY_FILE.write_text(json.dumps({
        "sessions": {},
        "runs": {}
    }, indent=2, ensure_ascii=False))
    print(f"✅ Đã tạo file memory mới: {MEMORY_FILE}")

# Khởi tạo memory database
memory_db = JsonMemoryDb(
    db_file=str(MEMORY_FILE),
    user_id="user_demo",
)


# ========================================
# 3. Tạo Agent
# ========================================
agent = Agent(
    model=OpenAIChat(
        id="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY")
    ),
    tools=[
        Function.from_callable(sum_1_to_n),
        Function.from_callable(calculator)
    ],
    instructions=[
        "Bạn là một trợ lý AI thông minh và hữu ích.",
        "Khi cần tính toán, hãy SỬ DỤNG TOOL thay vì tự tính.",
        "Luôn giải thích rõ ràng cách bạn sử dụng tool.",
        "Trả lời bằng tiếng Việt trừ khi được yêu cầu khác."
    ],
    memory=memory_db,
    show_tool_calls=True,  # Hiển thị khi agent gọi tool
    markdown=True,
)


# ========================================
# 4. Chạy Agent
# ========================================
def main():
    print("=" * 60)
    print("🤖 AGNO AGENT DEMO - GPT-4o-mini với Tools")
    print("=" * 60)
    print(f"📁 File memory: {MEMORY_FILE.absolute()}")
    print("=" * 60)
    print()
    
    # Câu hỏi demo
    questions = [
        "Hãy tính tổng các số từ 1 đến 100",
        "Tính 25.5 nhân với 4",
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n{'─' * 60}")
        print(f"❓ Câu hỏi {i}: {question}")
        print(f"{'─' * 60}\n")
        
        # Gọi agent
        response = agent.run(question)
        
        # In kết quả
        print(f"🤖 Agent trả lời:\n{response.content}\n")
    
    print("=" * 60)
    print("✅ Demo hoàn tất!")
    print(f"📝 Lịch sử hội thoại đã được lưu vào: {MEMORY_FILE.absolute()}")
    print("💡 Chạy lại script để thấy agent nhớ các câu hỏi trước!")
    print("=" * 60)


if __name__ == "__main__":
    # Kiểm tra API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ LỖI: Chưa set biến môi trường OPENAI_API_KEY!")
        print("Hãy xem lại phần 2 của hướng dẫn.")
        exit(1)
    
    main()
```

---

## 4. Nội Dung Mẫu của `memory.json`

File `memory.json` sẽ tự động được tạo khi chạy lần đầu với nội dung:

```json
{
  "sessions": {},
  "runs": {}
}
```

Sau khi chạy agent, file sẽ được cập nhật với lịch sử hội thoại:

```json
{
  "sessions": {
    "session_abc123": {
      "session_id": "session_abc123",
      "user_id": "user_demo",
      "messages": [
        {
          "role": "user",
          "content": "Hãy tính tổng các số từ 1 đến 100"
        },
        {
          "role": "assistant",
          "content": "Tổng các số từ 1 đến 100 là 5050"
        }
      ],
      "created_at": "2026-02-03T10:30:00",
      "updated_at": "2026-02-03T10:30:05"
    }
  },
  "runs": {
    "run_xyz789": {
      "run_id": "run_xyz789",
      "session_id": "session_abc123",
      "messages": [...],
      "tools_called": ["sum_1_to_n"]
    }
  }
}
```

---

## 5. Cách Chạy

```bash
# Đảm bảo đã activate Conda environment
# Windows & macOS/Linux:
conda activate agno-env

# Chạy demo
python main.py
```

**Kết quả mong đợi:**

```
============================================================
🤖 AGNO AGENT DEMO - GPT-4o-mini với Tools
============================================================
📁 File memory: /path/to/agno-demo/memory.json
============================================================

────────────────────────────────────────────────────────────
❓ Câu hỏi 1: Hãy tính tổng các số từ 1 đến 100
────────────────────────────────────────────────────────────

🤖 Agent trả lời:
Tổng các số từ 1 đến 100 là **5050**.

────────────────────────────────────────────────────────────
❓ Câu hỏi 2: Tính 25.5 nhân với 4
────────────────────────────────────────────────────────────

🤖 Agent trả lời:
Kết quả của 25.5 nhân với 4 là **102.0**.

============================================================
✅ Demo hoàn tất!
📝 Lịch sử hội thoại đã được lưu vào: /path/to/agno-demo/memory.json
💡 Chạy lại script để thấy agent nhớ các câu hỏi trước!
============================================================
```

---

## 6. Troubleshooting (Xử Lý Lỗi Thường Gặp)

### ❌ Lỗi 1: `AuthenticationError` - Thiếu hoặc sai API Key

**Triệu chứng:**
```
openai.AuthenticationError: Incorrect API key provided
```

**Nguyên nhân:** Chưa set hoặc set sai `OPENAI_API_KEY`.

**Giải pháp:**
1. Kiểm tra API key có đúng format `sk-...` không
2. Set lại biến môi trường:
   ```bash
   # Windows
   $env:OPENAI_API_KEY="sk-your-real-key-here"
   
   # macOS/Linux
   export OPENAI_API_KEY="sk-your-real-key-here"
   ```
3. Kiểm tra xem đã set đúng chưa:
   ```bash
   # Windows
   echo $env:OPENAI_API_KEY
   
   # macOS/Linux
   echo $OPENAI_API_KEY
   ```

---

### ❌ Lỗi 2: `command not found` - Sai cách activate conda environment

**Triệu chứng:**
```bash
python: command not found
# hoặc
pip: command not found
# hoặc
conda: command not found
```

**Nguyên nhân:** Chưa activate conda environment hoặc chưa cài conda.

**Giải pháp:**

**Bước 1:** Kiểm tra conda đã cài chưa:
```bash
conda --version
```

Nếu lỗi `conda: command not found`, cài Miniconda từ [docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)

**Bước 2:** Activate environment:
```bash
# Cả Windows và macOS/Linux đều dùng lệnh này
conda activate agno-env

# Kiểm tra đã activate chưa - dòng đầu terminal phải có (agno-env)
# Ví dụ: (agno-env) user@computer:~/agno-demo$
```

**Bước 3:** Nếu lỗi `CondaError: Run 'conda init' first`:
```bash
# Khởi tạo conda cho shell
conda init bash  # hoặc zsh, powershell

# Sau đó đóng và mở lại terminal
```

Sau khi activate đúng, prompt sẽ có `(agno-env)` ở đầu dòng.

---

### ❌ Lỗi 3: `ModuleNotFoundError: No module named 'agno'`

**Triệu chứng:**
```
ModuleNotFoundError: No module named 'agno'
```

**Nguyên nhân:** Package `agno` chưa được cài hoặc cài ở Python khác.

**Giải pháp:**
1. Đảm bảo đã activate conda environment (xem Lỗi 2)
2. Cài lại agno:
   ```bash
   pip install agno --upgrade
   ```
3. Kiểm tra danh sách package đã cài:
   ```bash
   conda list | grep agno
   # hoặc
   pip list | grep agno
   ```
4. Nếu vẫn lỗi, kiểm tra đúng Python nào đang dùng:
   ```bash
   which python  # macOS/Linux
   where python  # Windows
   ```
5. Kiểm tra environment hiện tại:
   ```bash
   conda info --envs
   # Dấu * cho biết environment nào đang active
   ```

---

### ❌ Lỗi 4: `SSL: CERTIFICATE_VERIFY_FAILED` - Lỗi SSL/Proxy

**Triệu chứng:**
```
ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
```

**Nguyên nhân:** Mạng công ty/trường học chặn SSL hoặc proxy cấu hình sai.

**Giải pháp:**

**Cách 1:** Set proxy (nếu có):
```bash
# Windows
$env:HTTP_PROXY="http://proxy.company.com:8080"
$env:HTTPS_PROXY="http://proxy.company.com:8080"

# macOS/Linux
export HTTP_PROXY="http://proxy.company.com:8080"
export HTTPS_PROXY="http://proxy.company.com:8080"
```

**Cách 2:** Tắt verify SSL (CHỈ dùng để test, không khuyến khích):
```python
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

**Cách 3:** Cài đặt certificates:
```bash
# macOS
/Applications/Python\ 3.x/Install\ Certificates.command

# Ubuntu/Debian
sudo apt-get install ca-certificates
```

---

### ❌ Lỗi 5: `TypeError` hoặc Import Error - Version Mismatch

**Triệu chứng:**
```
TypeError: __init__() got an unexpected keyword argument 'xxx'
# hoặc
ImportError: cannot import name 'OpenAIChat' from 'agno.models.openai'
```

**Nguyên nhân:** Version Python hoặc package không tương thích.

**Giải pháp:**

1. **Kiểm tra version Python:**
   ```bash
   python --version
   # Cần Python 3.8+, khuyến nghị 3.10 hoặc 3.11
   ```

2. **Cập nhật pip:**
   ```bash
   pip install --upgrade pip
   ```

3. **Cài lại agno và dependencies:**
   ```bash
   pip uninstall agno -y
   pip install agno --no-cache-dir
   ```

4. **Kiểm tra version agno:**
   ```bash
   pip show agno
   ```

5. **Nếu vẫn lỗi, tạo conda environment mới:**
   ```bash
   # Xóa environment cũ
   conda deactivate
   conda env remove -n agno-env
   
   # Tạo lại từ đầu
   conda create -n agno-env python=3.11 -y
   conda activate agno-env
   pip install agno
   ```

---

## 7. Các Bước Tiếp Theo

Sau khi chạy thành công demo, bạn có thể:

1. **Thêm tool mới** - Tạo các hàm Python phức tạp hơn
2. **Thay đổi instructions** - Điều chỉnh cách agent phản hồi
3. **Dùng model khác** - Thử `gpt-4`, `gpt-4-turbo`, hoặc `gpt-3.5-turbo`
4. **Tích hợp database** - Dùng PostgreSQL, SQLite thay vì JSON
5. **Xây dựng chatbot** - Tạo loop để chat liên tục với agent

---

## 8. Tài Liệu Tham Khảo

- **Agno Documentation:** https://docs.agno.com
- **OpenAI API Docs:** https://platform.openai.com/docs
- **Python venv:** https://docs.python.org/3/library/venv.html

---

## 9. Liên Hệ & Hỗ Trợ

Nếu gặp vấn đề:
1. Đọc kỹ phần **Troubleshooting** ở trên
2. Kiểm tra lại từng bước trong phần **Cài Đặt**
3. Google lỗi cụ thể (copy error message đầy đủ)
4. Hỏi trên diễn đàn/Slack/Discord của Agno

---

**Chúc bạn thành công! 🚀**
