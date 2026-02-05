# Báo Cáo Tích Hợp AgentLightning với AGNO

## 📋 Tổng Quan

Báo cáo này trình bày chi tiết về việc tích hợp **AgentLightning** (framework training từ Microsoft) với **AGNO** (framework xây dựng AI agents) để thực hiện training agents với thuật toán **APO (Automatic Prompt Optimization)**.

---


### 1.1 AgentLightning Framework

**AgentLightning** là framework từ Microsoft để training và cải thiện AI agents thông qua reinforcement learning.

#### Tính Năng Chính

- **Zero Code Change Integration**: Tích hợp với agents hiện có mà không cần thay đổi code nhiều
- **Multiple Algorithms**: Hỗ trợ RL, APO, Supervised Fine-tuning
- **Framework Agnostic**: Hoạt động với LangChain, AutoGen, CrewAI, hoặc custom agents
- **Continuous Learning**: Vòng lặp training liên tục để cải thiện hiệu suất

#### Kiến Trúc AgentLightning

```
┌──────────────────────────────────────────────┐
│          AgentLightning System               │
├──────────────────────────────────────────────┤
│                                              │
│  ┌────────────┐    ┌──────────────┐         │
│  │ Trainer    │───▶│ LightningStore│         │
│  │            │    │ (Tasks/Traces)│         │
│  └────────────┘    └──────────────┘         │
│         │                  │                 │
│         ▼                  ▼                 │
│  ┌────────────┐    ┌──────────────┐         │
│  │ Algorithm  │◀───│  Agent       │         │
│  │ (APO/RL)   │    │  Executor    │         │
│  └────────────┘    └──────────────┘         │
│         │                                    │
│         ▼                                    │
│  ┌────────────┐                             │
│  │ Updated    │                             │
│  │ Resources  │                             │
│  └────────────┘                             │
└──────────────────────────────────────────────┘
```

---

## 2. Thuật Toán APO (Automatic Prompt Optimization)

### 2.1 Khái Niệm & Cấu Hình Thực Tế
**APO (Automatic Prompt Optimization)** là kỹ thuật tối ưu hóa prompt tự động sử dụng LLM để "phê bình" và "chỉnh sửa" chính nó.

Trong dự án này, thuật toán APO được cấu hình cụ thể như sau (trong `rollout.py`):
- **Gradient Model**: `gpt-4o-mini` (Đóng vai trò Critic - Phân tích lỗi sai).
- **Edit Model**: `gpt-4o-mini` (Đóng vai trò Editor - Sửa lại prompt dựa trên phê bình).
- **Cơ chế**: Sử dụng "Textual Gradients" - thay vì đạo hàm số học như Deep Learning truyền thống, APO tạo ra các đạo hàm văn bản (lời phê bình) để định hướng việc sửa đổi.

### 2.2 Ví Dụ Thực Tế Từ Dữ Liệu Chạy
Dưới đây là ví dụ minh họa sự thay đổi của prompt qua quá trình huấn luyện thực tế (trích xuất từ `best_prompts.json`):

**Giai đoạn 1: Khởi động (Iteration 1)**
Hệ thống bắt đầu với một prompt cơ bản hoặc prompt tiếng Việt do người dùng cung cấp.
> **Prompt:** *"Bạn là một trợ lý AI giúp tôi giải quyết thắc mắc"*  
> **Reward:** 1.0 (Khởi điểm)

**Giai đoạn 2: Tối ưu hóa (Iteration 2 - Mô phỏng)**
Sau khi chạy qua các tasks thực tế, hệ thống nhận thấy prompt trên quá ngắn và thiếu hướng dẫn cụ thể khi gặp các câu hỏi toán học phức tạp.
> **Critique (Gradient):** "Prompt hiện tại quá chung chung. Agent thiếu hướng dẫn về việc giải thích từng bước (Chain-of-Thought) và định dạng câu trả lời rõ ràng."

> **Optimized Prompt (Candidate):**
> *"You are a helpful math assistant. Solve math problems step by step. When given a calculation task, use the available tools. Always show your work and provide the final answer clearly. Be accurate and precise in your calculations."*

**Kết quả:**
Các phiên bản prompt sau khi tối ưu (English version) thường có cấu trúc rõ ràng hơn, hướng dẫn agent thực hiện các bước suy luận cụ thể, từ đó nâng cao độ chính xác khi giải quyết các tác vụ phức tạp.

## 3. Kiến Trúc Hiện Tại Của Dự Án

### 3.1 Cấu Trúc Thư Mục

```
d:\Python\Agent\
├── core/                    # AGNO agent core
│   └── agno_memory.db      # Session và trace storage
├── training/               # AgentLightning training
│   ├── train.py           # Main orchestrator
│   ├── config.py          # Training configuration
│   ├── setup.py           # Infrastructure setup
│   ├── data/              # Data preparation
│   │   ├── data_preparation.py
│   │   ├── conversation_extractor.py
│   │   ├── conversation_to_dataset.py
│   │   └── dataset.py
│   ├── engine/            # Training execution
│   │   ├── training_executor.py
│   │   ├── trainer_factory.py
│   │   ├── rollout.py
│   │   └── grader.py
│   └── utils/             # Utilities
│       ├── infrastructure.py
│       ├── prompt_manager.py
│       ├── result_saver.py
│       └── otlp.py
├── app/                    # Streamlit UI
└── main.py                # Entry point
```

### 3.2 Luồng Training Hiện Tại

```python
# Từ train.py
def main():
    # 1. Initialize (Dependencies + Config + Infrastructure)
    agent_config, training_config, db = initialize_training()
    
    # 2. Prepare datasets
    train_dataset, val_dataset = prepare_datasets(training_config)
    
    # 3. Execute training
    trainer, initial_prompt = run_training(
        training_config, agent_config, db,
        train_dataset, val_dataset
    )
    
    # 4. Save results
    save_training_results(trainer, initial_prompt, training_config)
```

---

## 4. Tích Hợp OpenTelemetry & Tracing

### 4.1 Vai Trò Của OpenTelemetry
**OpenTelemetry (OTEL)** được sử dụng trong dự án để thu thập các **traces** (dấu vết thực thi) của Agent. Trong thuật toán **APO**, các traces này cực kỳ quan trọng vì:
- Cung cấp dữ liệu thô về quá trình suy nghĩ (reasoning) và gọi công cụ (tool calls).
- Cho phép **LLM Critic** phân tích chính xác Agent đã "sai" ở bước nào để tạo ra Critique chất lượng.
- Lưu trữ lịch sử thực thi để đối chiếu hiệu suất của Agent.

### 4.2 Cấu Hình OTLP Exporter
Dự án sử dụng `OTLPSpanExporter` để gửi dữ liệu traces đến **Lightning Store**.

**File cấu hình:** [otlp.py](file:///home/lamquy/Project/Agent_demo/training/utils/otlp.py)

```python
def setup_otlp_exporter(endpoint: str, service_name: str):
    # Khởi tạo TracerProvider
    resource = Resource(attributes={SERVICE_NAME: service_name})
    provider = TracerProvider(resource=resource)
    
    # Cấu hình Exporter gửi đến AgentLightning Store
    otlp_exporter = OTLPSpanExporter(endpoint=endpoint)
    provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    
    # Thiết lập làm Global Tracer
    trace.set_tracer_provider(provider)
```

### 4.3 Theo Dõi Traces (Dashboard)
Bạn có thể theo dõi các traces này trực quan thông qua dashboard bằng lệnh:
```bash
agl store --port 4747
```

---

## 5. Các Bước Tích Hợp AgentLightning với AGNO

### 5.1 Kiến Trúc Tích Hợp

```
┌─────────────────────────────────────────────────────────┐
│                AGNO + AgentLightning                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐         ┌────────────────┐           │
│  │ AGNO Agent   │◀────────│ APO Algorithm  │           │
│  │ (Executor)   │         │                │           │
│  └──────────────┘         └────────────────┘           │
│         │                         ▲                     │
│         │ Traces                  │ Updated             │
│         ▼                         │ Prompts             │
│  ┌──────────────┐         ┌────────────────┐           │
│  │ Lightning    │────────▶│ Trainer        │           │
│  │ Store        │         │                │           │
│  └──────────────┘         └────────────────┘           │
│         │                                               │
│         ▼                                               │
│  ┌──────────────┐                                      │
│  │ Training     │                                      │
│  │ Dataset      │                                      │
│  └──────────────┘                                      │
└─────────────────────────────────────────────────────────┘
```

### 5.2 Bước 1: Chuẩn Bị Môi Trường

#### a. Cài Đặt Dependencies

```bash
# Đã có trong requirements.txt
pip install agentlightning
pip install agno
pip install opentelemetry-api
pip install opentelemetry-sdk
```

#### b. Cấu Hình Environment Variables

```bash
# .env
OPENAI_API_KEY=your-api-key
AGENTOPS_API_KEY=your-agentops-key  # Optional, for tracing
AGENTOPS_LOG_LEVEL=DEBUG  # Optional, for debugging
```

### 5.3 Bước 2: Wrap AGNO Agent cho AgentLightning

#### Tạo Lightning-Compatible Agent Wrapper

```python
# training/agent_wrapper.py
from agentlightning import Agent
from agno import Agno
from opentelemetry import trace

class AgnoLightningAgent(Agent):
    """Wrapper để AGNO agent tương thích với AgentLightning."""
    
    def __init__(self, agent_config):
        super().__init__()
        
        # Khởi tạo AGNO agent
        self.agno_agent = Agno(
            model=agent_config.get("model", "gpt-4o-mini"),
            tools=agent_config.get("tools", []),
            memory=agent_config.get("memory", True),
            reasoning=True,
            markdown=True
        )
        
        # Prompt template có thể tune được
        self.system_prompt = agent_config.get(
            "system_prompt",
            "Bạn là một trợ lý AI giúp tôi giải quyết thắc mắc"
        )
    
    def run(self, task: str) -> dict:
        """
        Chạy agent trên task và trả về kết quả với tracing.
        
        AgentLightning sẽ:
        1. Gọi run() với task
        2. Thu thập traces
        3. Tính reward
        4. Dùng APO để cải thiện system_prompt
        """
        tracer = trace.get_tracer(__name__)
        
        with tracer.start_as_current_span("agno_agent_run") as span:
            span.set_attribute("task", task)
            span.set_attribute("system_prompt", self.system_prompt)
            
            # Chạy AGNO agent
            response = self.agno_agent.run(
                task,
                system_prompt=self.system_prompt
            )
            
            # Extract result
            result = {
                "answer": response.content,
                "reasoning": getattr(response, "reasoning", ""),
                "tool_calls": getattr(response, "tool_calls", [])
            }
            
            span.set_attribute("answer", result["answer"])
            
            return result
    
    def update_resource(self, resource_name: str, resource_value):
        """
        AgentLightning gọi method này để update prompt sau mỗi iteration.
        """
        if resource_name == "system_prompt":
            self.system_prompt = resource_value
            print(f"✅ Updated system_prompt to:\n{resource_value}\n")
```

### 5.4 Bước 3: Cấu Hình Training cho APO

```python
# training/config.py (cập nhật)
from dataclasses import dataclass

@dataclass
class TrainingConfig:
    """Cấu hình training với APO."""
    
    # === AgentLightning Settings ===
    otlp_endpoint: str = "http://localhost:4318/v1/traces"
    agent_id: str = "agno-agent-v1"
    n_runners: int = 8  # Số lượng parallel runners
    max_iterations: int = 10  # Số iterations cho APO
    
    # === APO Algorithm Settings ===
    algorithm: str = "apo"
    learning_rate: float = 0.001
    
    # Critic LLM (đánh giá prompt)
    critic_model: str = "gpt-4"
    critic_temperature: float = 0.7
    
    # Editor LLM (sửa prompt)
    editor_model: str = "gpt-4"
    editor_temperature: float = 0.5
    
    # === Reward Settings ===
    use_llm_grader: bool = True  # Dùng LLM để grade responses
    reward_tolerance: float = 0.1
    
    # === Dataset Settings ===
    task_type: str = "conversation"
    use_real_data: bool = True
    user_data_db_path: str = "core/agno_memory.db"
    max_real_data_age_days: int = 30
```

### 5.5 Bước 4: Chuẩn Bị Training Dataset

Quy trình chuẩn bị dữ liệu được thiết kế để tận dụng tối đa lịch sử tương tác thực tế từ người dùng (Real User Data). Hệ thống tự động kết nối tới cơ sở dữ liệu bộ nhớ của AGNO (`agno_memory.db`) để trích xuất các phiên hội thoại gần nhất. Mỗi tin nhắn của người dùng sẽ được tách thành một nhiệm vụ huấn luyện (Task) độc lập, loại bỏ các nhiễu loạn không cần thiết. Sau đó, dữ liệu được chia thành tập Train và Validation (80/20). Việc sử dụng dữ liệu thực tế này giúp thuật toán APO tối ưu hóa prompt sát sườn với nhu cầu và ngữ cảnh cụ thể mà người dùng thường xuyên truy vấn, đảm bảo tính ứng dụng cao cho Agent.

**Ví dụ cấu trúc Task sau khi chuyển đổi:**
```json
{
  "question": "Làm sao để cài đặt AgentLightning?",
  "task_id": "real_session_e9d8f7_msg_2"
}
```

### 5.6 Bước 5: Setup Training Pipeline

```python
# training/train.py (cập nhật)
from agentlightning import Trainer
from .agent_wrapper import AgnoLightningAgent

def run_training(training_config, agent_config, db, 
                 train_dataset, val_dataset, store_url=None):
    """Execute APO training."""
    
    # 1. Tạo agent wrapper
    agent = AgnoLightningAgent(agent_config)
    
    # 2. Define tunable resources
    resources = {
        "system_prompt": agent.system_prompt  # Initial prompt
    }
    
    # 3. Tạo trainer với APO algorithm
    trainer = Trainer(
        agent=agent,
        algorithm="apo",
        resources=resources,
        config={
            "critic_model": training_config.critic_model,
            "editor_model": training_config.editor_model,
            "max_iterations": training_config.max_iterations,
            "n_runners": training_config.n_runners
        },
        store_url=store_url  # Optional external store
    )
    
    # 4. Chạy training
    print("🚀 Starting APO Training...")
    results = trainer.train(
        train_dataset=train_dataset,
        val_dataset=val_dataset
    )
    
    # 5. Lấy optimized prompt
    optimized_prompt = trainer.get_best_resource("system_prompt")
    
    return trainer, optimized_prompt
```

---

## 6. Ý Tưởng Training

### 6.1 Mục Tiêu Training

1. **Cải thiện chất lượng response**
   - Trả lời chính xác hơn
   - Giải thích rõ ràng hơn
   - Reasoning tốt hơn

2. **Tối ưu hóa prompt**
   - Tự động tìm prompt tốt nhất
   - Không cần manual tuning
   - Adapt theo domain cụ thể

3. **Học từ real user data**
   - Sử dụng conversations thật từ users
   - Cải thiện theo feedback thực tế

### 6.2 Training Strategy

#### Strategy 1: Domain-Specific Training

```python
# Train cho từng domain riêng
domains = ["math", "conversation", "code_generation"]

for domain in domains:
    domain_dataset = filter_by_domain(full_dataset, domain)
    initial_prompt = get_domain_prompt(domain)
    trainer.train(domain_dataset, initial_prompt)
```

#### Strategy 2: Progressive Training

```python
# Training theo độ khó tăng dần
difficulty_levels = ["easy", "medium", "hard"]

current_prompt = initial_prompt
for level in difficulty_levels:
    level_dataset = filter_by_difficulty(full_dataset, level)
    trainer.train(level_dataset, current_prompt)
```

### 6.3 Reward Function Design

```python
# training/engine/grader.py
def calculate_reward(task, agent_response, expected_answer):
    """
    Tính reward cho agent response.
    
    Returns:
        float: Reward từ 0.0 đến 1.0
    """
    # 1. Accuracy score (40%)
    accuracy = check_accuracy(agent_response, expected_answer)
    
    # 2. Reasoning quality (60%)
    reasoning = grade_reasoning(agent_response)
    
    return 0.4 * accuracy + 0.6 * reasoning
```

---

## 7. Chuẩn Bị Câu Hỏi / Dataset

### 7.1 Nguyên Tắc Chuẩn Bị Dataset

#### ✅ DO (Nên Làm)

1. **Đa dạng (Diversity)**
   - Cover nhiều topic khác nhau
   - Nhiều difficulty levels

2. **Cân đối (Balance)**
   - Số lượng examples đều nhau
   - Tránh bias về một loại câu hỏi

3. **Real-world Representative**
   - Giống câu hỏi users thật sẽ hỏi

#### ❌ DON'T (Tránh)

1. ❌ Dataset quá nhỏ (< 50 examples)
2. ❌ Chỉ một loại câu hỏi
3. ❌ Expected answers mơ hồ

### 7.2 Template Chuẩn Bị Câu Hỏi

#### Template 1: Question-Answering

```json
{
  "task": "What is machine learning?",
  "expected_answer": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed.",
  "context": "AI/ML basics",
  "difficulty": "medium",
  "category": "definition",
  "requires_reasoning": false
}
```

#### Template 2: Problem Solving

```json
{
  "task": "A train travels 120 km in 2 hours. What is its average speed?",
  "expected_answer": "60 km/h (calculated as 120 km ÷ 2 hours)",
  "context": "Basic math",
  "difficulty": "easy",
  "category": "math",
  "requires_reasoning": true,
  "reasoning_steps": [
    "Identify given: distance = 120 km, time = 2 hours",
    "Apply formula: speed = distance / time",
    "Calculate: 120 / 2 = 60 km/h"
  ]
}
```

#### Template 3: Multi-step Reasoning

```json
{
  "task": "If all roses are flowers, and some flowers fade quickly, can we conclude that some roses fade quickly?",
  "expected_answer": "No, we cannot conclude that. While all roses are flowers, we don't know if roses are among the flowers that fade quickly.",
  "context": "Logic reasoning",
  "difficulty": "hard",
  "category": "logical_reasoning",
  "requires_reasoning": true,
  "reasoning_type": "deductive"
}
```

### 6.3 Ví Dụ Dataset Hoàn Chỉnh

```python
# training_dataset.json
[
    # === Easy Questions (30%) ===
    {
        "task": "What is 2 + 2?",
        "expected_answer": "4",
        "context": "Basic arithmetic",
        "difficulty": "easy",
        "category": "math"
    },
    {
        "task": "What is the capital of Vietnam?",
        "expected_answer": "Hanoi",
        "context": "Geography",
        "difficulty": "easy",
        "category": "factual"
    },
    
    # === Medium Questions (50%) ===
    {
        "task": "Explain the difference between supervised and unsupervised learning.",
        "expected_answer": "Supervised learning uses labeled data to train models, while unsupervised learning finds patterns in unlabeled data.",
        "context": "Machine Learning",
        "difficulty": "medium",
        "category": "explanation"
    },
    {
        "task": "Calculate the area of a circle with radius 5 cm.",
        "expected_answer": "78.54 cm² (using formula πr² = 3.14159 × 5²)",
        "context": "Geometry",
        "difficulty": "medium",
        "category": "math",
        "requires_reasoning": true
    },
    
    # === Hard Questions (20%) ===
    {
        "task": "Analyze the time complexity of a recursive Fibonacci implementation and suggest optimization.",
        "expected_answer": "The recursive approach has O(2^n) time complexity due to redundant calculations. Optimization: use memoization or dynamic programming to achieve O(n).",
        "context": "Computer Science",
        "difficulty": "hard",
        "category": "analysis",
        "requires_reasoning": true
    }
]
```

### 6.4 Tools để Tạo Dataset

#### Script Tự Động Tạo Dataset

```python
# tools/dataset_generator.py
import json
from typing import List, Dict

class DatasetGenerator:
    """Tool để tạo và validate training dataset."""
    
    def __init__(self):
        self.dataset = []
    
    def add_question(self, task: str, expected_answer: str,
                     difficulty: str, category: str, **kwargs):
        """Thêm câu hỏi vào dataset."""
        question = {
            "task": task,
            "expected_answer": expected_answer,
            "difficulty": difficulty,
            "category": category,
            **kwargs
        }
        self.dataset.append(question)
    
    def validate(self) -> bool:
        """Validate dataset."""
        # Check minimum size
        if len(self.dataset) < 50:
            print("⚠️ Dataset quá nhỏ, nên có ít nhất 50 examples")
            return False
        
        # Check balance
        difficulties = [q["difficulty"] for q in self.dataset]
        easy_pct = difficulties.count("easy") / len(difficulties)
        medium_pct = difficulties.count("medium") / len(difficulties)
        hard_pct = difficulties.count("hard") / len(difficulties)
        
        print(f"Distribution: Easy {easy_pct:.0%}, Medium {medium_pct:.0%}, Hard {hard_pct:.0%}")
        
        return True
    
    def save(self, filepath: str):
        """Lưu dataset ra file."""
        if self.validate():
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.dataset, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved {len(self.dataset)} questions to {filepath}")

# Usage
generator = DatasetGenerator()

# Thêm questions
generator.add_question(
    task="What is Python?",
    expected_answer="Python is a high-level programming language...",
    difficulty="easy",
    category="definition"
)

# Save
generator.save("training_dataset.json")
```

### 6.5 Cách Lấy Dataset từ Real User Data

```python
# training/data/extract_from_real_data.py
import sqlite3
from datetime import datetime, timedelta

def extract_user_conversations(db_path: str, days: int = 30) -> List[Dict]:
    """
    Extract conversations từ AGNO memory database.
    
    Args:
        db_path: Path to agno_memory.db
        days: Lấy data từ bao nhiêu ngày gần đây
    
    Returns:
        List of training examples
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Lấy conversations gần đây
    cutoff_date = datetime.now() - timedelta(days=days)
    
    query = """
    SELECT user_message, agent_response, timestamp, rating
    FROM conversations
    WHERE timestamp > ?
    AND rating >= 4  -- Chỉ lấy conversations có rating tốt
    ORDER BY timestamp DESC
    """
    
    cursor.execute(query, (cutoff_date,))
    rows = cursor.fetchall()
    
    dataset = []
    for row in rows:
        user_msg, agent_resp, timestamp, rating = row
        dataset.append({
            "task": user_msg,
            "expected_answer": agent_resp,
            "context": "real_user_conversation",
            "difficulty": "medium",  # Can be inferred
            "category": "conversation",
            "timestamp": timestamp,
            "user_rating": rating
        })
    
    conn.close()
    
    print(f"✅ Extracted {len(dataset)} conversations from last {days} days")
    return dataset
```

---



---


## 8. Quy Trình Training Đầy Đủ

### 8.1 Checklist Trước Khi Training

- [ ] Environment variables đã setup (OPENAI_API_KEY, etc.)
- [ ] Dependencies đã cài đặt
- [ ] Training dataset đã chuẩn bị (≥ 50 examples)
- [ ] Validation dataset đã chuẩn bị (≥ 20 examples)
- [ ] Initial prompt đã viết
- [ ] Reward function đã config
- [ ] Training config đã review

### 8.2 Command để Chạy Training

```bash
# Dry run (test setup)
python -m training.train --dry-run

# Training với default config
python -m training.train --iterations 10 --algorithm apo

# Training với custom config
python -m training.train \
    --iterations 20 \
    --algorithm apo \
    --real-data-db "core/agno_memory.db"

# Training với external store (dashboard)
python -m training.train \
    --iterations 10 \
    --algorithm apo \
    --store-url "http://localhost:4747"
```

### 8.3 Monitoring Training

```python
# Training output sẽ có dạng:
"""
🚀 Starting APO Training...

Iteration 1/10:
  Current Prompt: "You are a helpful assistant."
  Avg Reward: 0.65
  
Iteration 2/10:
  Critic: "Prompt lacks specificity..."
  Editor: Adding step-by-step guidance
  Updated Prompt: "You are a helpful assistant. Think carefully..."
  Avg Reward: 0.72 ↑
  
...

Iteration 10/10:
  Avg Reward: 0.89 ↑
  
✅ Training Complete!
"""
```

### 8.4 Sau Training

```python
# 1. Load optimized prompt từ prompt manager
from training.utils.prompt_manager import PromptManager
pm = PromptManager()
best_record = pm.load_best_prompt()
optimized_prompt = best_record.prompt_text

# 2. Update agent với prompt mới
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=optimized_prompt.split("\n"),
    # ... các config khác
)
```

---

## 9. Best Practices & Tips

### 9.1 Training Tips

1. **Start Simple**
   - Bắt đầu với prompt đơn giản
   - Dataset nhỏ (~10 examples) để test setup
   - Ít iterations (~2-3) để validate reward logic

2. **Iterate Gradually**
   - Tăng dần dataset size khi hệ thống đã ổn định
   - Monitor reward curves trên dashboard
   - Kiểm tra xem prompt sinh ra có bị "lặp" hay không

3. **Diversity Matters**
   - Dataset nên bao gồm cả những trường hợp Agent thường trả lời sai
   - Đảm bảo câu hỏi bao quát các tình huống thực tế mà User hay gặp

4. **Reward Engineering**
   - Nếu dùng LLM Grader, hãy đảm bảo mẫu chấm điểm (Grading Prompt) thật rõ ràng
   - Reward 0.0 có thể do lỗi runtime hoặc Agent không trả lời đúng format

### 9.2 Common Pitfalls

❌ **Tránh những lỗi này:**

1. **Overfitting**
   - Dataset quá nhỏ nhưng iterations quá cao dẫn đến prompt bị tối ưu hóa quá mức cho vài câu hỏi cụ thể.

2. **Poor Reward Signal**
   - Grader quá lỏng lẻo (luôn cho 1.0) hoặc quá khắt khe (luôn cho 0.0).

3. **Infrastructure Issues**
   - OTLP endpoint không chạy khiến AgentLightning không thu thập được traces để phân tích lỗi.

### 9.3 Debugging Guide

```python
# Xem dashboard để debug traces
# agl store --port 4747

# Kiểm tra logs chi tiết
# tail -f training/logs/training.log

# Kiểm tra database real data
# python -m training.data.data_preparation (chạy script lẻ)
```

---

## 10. Tài Nguyên Tham Khảo

### 10.1 Documentation

- [AgentLightning Docs](https://microsoft.github.io/agentlightning/)
- [AGNO Docs](https://docs.agno.com/)
- [APO Paper](https://arxiv.org/abs/2309.03409)
- [OpenTelemetry Tracing](https://opentelemetry.io/docs/)

### 10.2 Công cụ hỗ trợ
- **AgentOps**: Để quan sát (observability) nâng cao trong production.
- **SQLite Browser**: Để kiểm tra `agno_memory.db`.

---

## 11. Kết Luận

### 11.1 Tóm Tắt

Tích hợp **AgentLightning** mang lại khả năng **tự động hóa hoàn toàn** việc viết prompt. Thay vì "đoán" xem prompt nào tốt, hệ thống sẽ tự thử nghiệm, tự soi lỗi qua **OpenTelemetry Traces** và tự sửa mình.

### 11.2 Thành Phẩm Đạt Được
- Hệ thống trích xuất dữ liệu thực tế từ AGNO.
- Quy trình chấm điểm linh hoạt không cần đáp án mẫu.
- Cơ chế lưu trữ lịch sử prompts và kết quả training rõ ràng.
- Tận dụng sức mạnh của distributed tracing để phân tích lỗi sâu.

**Hệ thống hiện đã sẵn sàng cho giai đoạn huấn luyện quy mô lớn.** 🚀
