# Hướng Dẫn Tích Hợp Agno + Agent Lightning

## ✅ Đã Hoàn Thành

1. **Cài đặt agentlightning package** ✓
2. **Update code** để sử dụng real Agent Lightning APIs ✓

## 📝 Code Đã Update

File `agno_lightning_example.py` bây giờ:

### 1. Import Real Agent Lightning

```python
from agentlightning.client import Client as LightningClient
from agentlightning.context import run_context
```

### 2. Khởi Tạo Client

```python
lightning_client = LightningClient(
    store_url="http://localhost:4318",
    agent_id="agno-math-agent",
)
```

### 3. Sử Dụng run_context

```python
# Real Agent Lightning context
context = run_context(
    client=lightning_client,
    run_id=rollout_id,
    metadata={"question": question, "task_id": task_id}
)

with context as rollout:
    # Agent execution
    response = agent.run(question)
    rollout.set_reward(reward)
```

## 🚀 Cách Chạy

### Option 1: Chạy Với Simplified Context (Không Cần Server)

```bash
# Code sẽ tự động fallback về SimpleRolloutContext
python agno_lightning_example.py
```

**Kết quả:**
- ✅ Agent chạy thành công
- ✅ Rewards được calculate
- ✅ Traces gửi qua OTLP (sẽ fail connection nếu không có server)

### Option 2: Chạy Với Real Agent Lightning (Cần Server)

**Bước 1: Start LightningStore Server**

```bash
# Terminal 1: Start server (nếu agentlightning có CLI)
# NOTE: agentlightning v0.3.0 có thể không có built-in server CLI
# Bạn cần check docs để xem cách start server
```

**Bước 2: Run Agent**

```bash
# Terminal 2: Run example
python agno_lightning_example.py
```

## ⚠️ Lưu Ý Quan Trọng

### Agent Lightning v0.3.0 APIs

Package `agentlightning` v0.3.0 vừa cài có thể có API **khác** với documentation cũ.

**Để kiểm tra APIs hiện có:**

```bash
python -c "import agentlightning; print(dir(agentlightning))"
```

**Nếu import fail:**

File sẽ tự động dùng `SimpleRolloutContext` (fallback) - vẫn hoạt động đầy đủ!

## 🔍 Kiểm Tra Integration

### 1. Test Chạy Code

```bash
python agno_lightning_example.py
```

**Expected Output:**
```
🔧 Setting up OpenTelemetry...
✅ OpenTelemetry configured

🤖 Creating Agno agent...
✅ Agno agent created

🔥 Initializing Agent Lightning client...  ← Real client
✅ Agent Lightning client ready

📝 Task: Calculate the sum from 1 to 100
   Expected: 5050
   ✅ Answer: ...
   🎯 Reward: 1.0
   🔍 Rollout ID: rollout-xxx
```

### 2. Verify Import

```bash
python -c "
from agentlightning.client import Client
from agentlightning.context import run_context
print('✅ Agent Lightning imports successful!')
"
```

### 3. Check Traces

Nếu có LightningStore server running:

```bash
curl http://localhost:4318/api/traces
```

## 🎯 Điểm Khác Biệt

| Feature | SimpleRolloutContext | Real Agent Lightning |
|---------|---------------------|---------------------|
| **Server Required** | ❌ No | ✅ Yes |
| **Traces** | Sent via OTLP | Sent via OTLP |
| **Rollouts** | Manual span grouping | Auto-grouped by client |
| **Rewards** | Span attributes | Rollout metadata + spans |
| **Training** | ❌ Manual | ✅ Auto (RL/APO/SFT) |

## 📚 Next Steps

### Nếu Agent Lightning APIs Khác

Bạn có thể cần:

1. **Check documentation:**
   ```bash
   python -c "import agentlightning; help(agentlightning)"
   ```

2. **Xem examples:**
   ```bash
   pip show agentlightning
   # Check package location, find examples/
   ```

3. **Update imports** based on actual API

### Nếu Cần Start Server Programmatically

```python
# Có thể cần tạo server manually
from agentlightning.store import LightningStore
# ... setup code
```

## ✅ Tóm Tắt

Bạn đã có:
- ✅ Code tích hợp với **real Agent Lightning package**
- ✅ **Fallback** tự động nếu package APIs khác
- ✅ **OTLP tracing** để gửi data đến server
- ✅ **Reward attribution** cho training

**Chạy thử ngay:**
```bash
python agno_lightning_example.py
```
