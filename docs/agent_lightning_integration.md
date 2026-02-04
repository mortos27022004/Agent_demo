# Tích Hợp Agent Lightning với Agno thông qua OpenTelemetry

## Tổng Quan

Tài liệu này mô tả cách tích hợp **Agent Lightning** (training framework) với **Agno** (AI agent framework) sử dụng **OpenTelemetry** để tracing.

## Kiến Trúc

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Agent Lightning│◄────│  OpenTelemetry   │◄────│   Agno Agent    │
│   (Training)    │     │    (Tracing)     │     │  (Execution)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

## Files Đã Implement

### 1. `training/otlp.py` - OTLP Exporter Setup

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

def setup_otlp_exporter(endpoint, service_name):
    resource = Resource(attributes={SERVICE_NAME: service_name})
    provider = TracerProvider(resource=resource)
    otlp_exporter = OTLPSpanExporter(endpoint=endpoint)
    provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    trace.set_tracer_provider(provider)
    return provider
```

### 2. `training/rollout.py` - Agent Lightning Rollout

```python
import agentlightning as agl

@agl.rollout
def agno_agent_rollout(task, prompt_template, config, db):
    agent = create_agent_with_prompt(prompt_template, config, db)
    response = agent.run(task["question"])
    reward = calculate_reward(response.content, task["expected_answer"])
    return reward
```

### 3. `training/train.py` - Training Entry Point

```python
# Setup OTLP
otlp_provider = setup_otlp_exporter(
    endpoint="http://localhost:4318/v1/traces",
    service_name="agno-agent-training"
)

# Setup Trainer với APO algorithm
trainer = setup_trainer(initial_prompt, algorithm_type="apo")

# Run Training
trainer.fit(
    agent=agno_agent_rollout,
    train_dataset=train_dataset,
    val_dataset=val_dataset
)
```

## Flow Tích Hợp

```
1. Setup OTLP Exporter
   └─► Kết nối tới Agent Lightning collector

2. Generate Dataset
   └─► Math tasks với expected answers

3. Rollout Function (@agl.rollout)
   ├─► Nhận prompt_template từ Agent Lightning
   ├─► Tạo Agno Agent với prompt
   ├─► Chạy agent trên task
   ├─► Tính reward
   └─► Return reward → Agent Lightning

4. Agent Lightning APO
   ├─► Thu thập rewards từ tất cả rollouts
   ├─► Optimize prompt dựa trên rewards
   └─► Iterate cho đến convergence

5. Save Best Prompt
   └─► PromptManager lưu prompt với highest reward
```

## Dependencies

```txt
agentlightning>=0.3.0
opentelemetry-api
opentelemetry-sdk
opentelemetry-exporter-otlp
agno
```

## Usage

```bash
# Basic training
python training/train.py

# Custom parameters
python training/train.py --iterations 20 --algorithm apo

# Dry run (test setup)
python training/train.py --dry-run
```

## Key Components

| Component | File | Role |
|-----------|------|------|
| OTLP Setup | `otlp.py` | Configure OpenTelemetry |
| Rollout | `rollout.py` | Bridge Agno ↔ Agent Lightning |
| Trainer | `train.py` | Orchestrate training |
| Grader | `grader.py` | Calculate rewards |
| PromptManager | `prompt_manager.py` | Persist best prompts |

## Kết Quả

- ✅ Agent Lightning có thể train Agno agents
- ✅ OpenTelemetry traces được gửi cho monitoring
- ✅ Prompts được optimize qua APO algorithm
- ✅ Best prompts được lưu cho production use
