# Quick Start Guide - Chạy Full Chức Năng

## 🎯 Tổng Quan

Hệ thống có **2 chức năng chính:**
1. **Agent cơ bản** - Chạy Agno agent với tools
2. **Training system** - Train agent với Agent Lightning

---

## 📋 Prerequisites

### 1. Kiểm tra Dependencies

```bash
# Kiểm tra Python version
python --version  # Cần >= 3.8

# Kiểm tra packages đã cài
pip list | grep -E "agno|openai|agentlightning"
```

### 2. Setup Environment

```bash
# Tạo .env file nếu chưa có
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
EOF
```

### 3. Install Dependencies (nếu chưa có)

```bash
pip install -r requirements.txt
```

---

## 🚀 Option 1: Chạy Agent Cơ Bản

### Chức năng
- Chạy Agno agent với OpenAI
- Sử dụng tools: `sum_1_to_n`, `calculator`
- Lưu memory vào database
- OpenTelemetry tracing

### Cách chạy

```bash
# Chạy main agent
python main.py
```

### Expected Output

```
============================================================
📁 Database: /path/to/agno_memory.db
============================================================

────────────────────────────────────────────────────────────
❓ Câu hỏi 1: Tôi vừa hỏi bạn câu gì? Kết quả là bao nhiêu?
────────────────────────────────────────────────────────────

🤖 Agent trả lời:
[Agent response with tool usage]

============================================================
✅ Demo hoàn tất!
📝 Lịch sử hội thoại đã được lưu vào: /path/to/agno_memory.db
============================================================
```

### Customize Questions

Edit `main.py`, dòng 44-46:

```python
questions = [
    "Calculate the sum from 1 to 100",
    "What is 15 + 27?",
    # Add your questions here
]
```

---

## 🎓 Option 2: Chạy Training System

### Chức năng
- Train agent tự động với Agent Lightning
- APO algorithm optimize prompts
- OTLP tracing
- Reward-based learning

### Step 1: Dry Run (Test Setup)

```bash
# Test setup không train thật
python -m training.train --dry-run
```

**Expected Output:**
```
============================================================
🚀 Agno Agent Training with Agent Lightning
============================================================

✅ Agent Lightning is available
📊 Configuration:
   - Algorithm: apo
   - Iterations: 10
   - Train size: 20
   - Val size: 10

🔧 Setting up OTLP exporter...
✅ OTLP exporter configured

💾 Setting up database...
✅ Database: agno_memory_training.db

📝 Generating datasets...
✅ Generated 20 training tasks

🧪 DRY RUN MODE - Skipping actual training
✅ Setup complete!
```

### Step 2: Run Full Training

#### Basic Training (default settings)

```bash
python -m training.train
```

#### Custom Training

```bash
# Train với custom parameters
python -m training.train \
    --iterations 20 \
    --train-size 50 \
    --val-size 20 \
    --algorithm apo
```

**Parameters:**
- `--iterations N`: Số lượng training iterations (default: 10)
- `--train-size N`: Kích thước training dataset (default: 20)
- `--val-size N`: Kích thước validation dataset (default: 10)
- `--algorithm`: Thuật toán training: `apo`, `sft`, hoặc `rl` (default: apo)
- `--dry-run`: Test setup không train

### Expected Training Output

```
🚀 Starting Agent Lightning training...
============================================================

Iteration 1/10: Training...
  Task task_0000: Expected=1035, Got=1035, Reward=1.00
  Task task_0001: Expected=4005, Got=4005, Reward=1.00
  ...
  Average Reward: 0.65

Iteration 2/10: Training...
  Average Reward: 0.78

...

Iteration 10/10: Training...
  Average Reward: 0.95

============================================================
✅ Training complete!
📊 Results saved to: agno_memory_training.db
============================================================
```

---

## 🔧 Advanced: Monitor Training với Jaeger (Optional)

### Setup Jaeger OTLP Collector

```bash
# Start Jaeger container
docker run -d \
  --name jaeger \
  -p 4318:4318 \
  -p 16686:16686 \
  jaegertracing/all-in-one:latest
```

### Run Training với Jaeger

```bash
# Training sẽ tự động gửi traces đến Jaeger
python -m training.train
```

### View Traces

```bash
# Mở Jaeger UI
open http://localhost:16686

# Hoặc
xdg-open http://localhost:16686
```

---

## 📊 Kiểm Tra Kết Quả

### View Training Database

```bash
# List database files
ls -la agno_memory_training.db/

# View sessions
cat agno_memory_training.db/agno_sessions.json | jq

# View runs
cat agno_memory_training.db/agno_runs.json | jq

# View spans (traces)
cat agno_memory_training.db/agno_spans.json | jq
```

### View Agent Database

```bash
# Agent cơ bản database
ls -la agno_memory.db/

cat agno_memory.db/agno_sessions.json | jq
```

---

## 🎯 Use Cases & Examples

### Use Case 1: Test Agent Nhanh

```bash
# Chạy agent với 1 câu hỏi
python main.py
```

### Use Case 2: Train Agent Nhỏ

```bash
# Quick training với dataset nhỏ
python -m training.train --iterations 5 --train-size 10
```

### Use Case 3: Full Training Production

```bash
# Training đầy đủ với dataset lớn
python -m training.train \
    --iterations 50 \
    --train-size 100 \
    --val-size 30 \
    --algorithm apo
```

### Use Case 4: Experiment với Different Algorithms

```bash
# Test APO
python -m training.train --algorithm apo --iterations 10

# Test SFT
python -m training.train --algorithm sft --iterations 10

# Test RL
python -m training.train --algorithm rl --iterations 10
```

---

## ⚠️ Troubleshooting

### Problem 1: ModuleNotFoundError

```bash
# Missing agno
pip install agno==2.4.7

# Missing agentlightning
pip install agentlightning>=0.3.0

# Missing OpenTelemetry
pip install opentelemetry-api opentelemetry-sdk
```

### Problem 2: OpenAI API Key Error

```bash
# Check .env file
cat .env

# Make sure it has:
# OPENAI_API_KEY=sk-...

# Reload env
source .env  # hoặc
export $(cat .env | xargs)
```

### Problem 3: OTLP Connection Failed

**This is OK!** Training vẫn chạy được mà không cần OTLP collector.

Nếu muốn xem traces, start Jaeger:
```bash
docker run -d -p 4318:4318 -p 16686:16686 jaegertracing/all-in-one
```

### Problem 4: Training quá chậm

```bash
# Giảm dataset size
python -m training.train --train-size 10 --val-size 5

# Giảm iterations
python -m training.train --iterations 5
```

---

## 📖 Documentation

- [Agent Lightning Setup](docs/AGENT_LIGHTNING_SETUP.md)
- [Training Flow](docs/TRAINING_FLOW.md)
- [Module Structure](docs/MODULE_STRUCTURE.md)

---

## 🎉 Summary

**Để chạy full chức năng hệ thống:**

### Quick Start (Recommended)

```bash
# 1. Chạy agent cơ bản
python main.py

# 2. Test training setup
python -m training.train --dry-run

# 3. Run full training
python -m training.train
```

### Full Production Setup

```bash
# 1. Install all dependencies
pip install -r requirements.txt

# 2. Setup environment
echo "OPENAI_API_KEY=your_key" > .env

# 3. (Optional) Start Jaeger
docker run -d -p 4318:4318 -p 16686:16686 jaegertracing/all-in-one

# 4. Run agent
python main.py

# 5. Run training
python -m training.train --iterations 20 --train-size 50

# 6. (Optional) View traces
open http://localhost:16686
```

**Chúc bạn thành công! 🚀**
