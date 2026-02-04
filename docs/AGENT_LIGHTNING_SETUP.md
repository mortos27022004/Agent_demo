# Agent Lightning Integration - Setup Guide

## 📋 Tổng Quan

Integration này cho phép train Agno Agent tự động sử dụng **Agent Lightning** framework với **OpenTelemetry** traces.

## 🔧 Components

### Core Files
- `training_config.py` - Training configuration
- `otlp_setup.py` - OpenTelemetry OTLP exporter setup
- `dataset_generator.py` - Generate training datasets
- `reward_grader.py` - Reward calculation and grading
- `training.py` - Agent Lightning rollout function
- `train_agent.py` - Main training script
- `agent_manager.py` - Enhanced với custom prompt support

## 📦 Installation

### Step 1: Install Dependencies

```bash
# Install Agent Lightning and OpenTelemetry packages
pip install -r requirements.txt
```

**Required packages:**
- `agentlightning>=0.3.0`
- `opentelemetry-api==1.39.1`
- `opentelemetry-sdk==1.39.1`
- `opentelemetry-exporter-otlp-proto-http==1.39.1`
- `opentelemetry-exporter-otlp==1.39.1`
- `opentelemetry-semantic-conventions==0.60b1`
- `openinference-instrumentation-openai>=0.1.0`

### Step 2: Verify Installation

```bash
python -c "import agentlightning; print('✅ Agent Lightning installed')"
python -c "from opentelemetry import trace; print('✅ OpenTelemetry installed')"
```

## 🚀 Usage

### Dry Run (Test Setup)

```bash
python train_agent.py --dry-run
```

**Expected output:**
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
✅ OTLP exporter configured: http://localhost:4318/v1/traces

💾 Setting up database...
✅ Database: /path/to/agno_memory_training.db

📝 Generating datasets...
✅ Generated 20 training tasks
✅ Generated 10 validation tasks

📋 Sample tasks:
   - Calculate the sum from 1 to 45 → 1035
   - Calculate the sum from 1 to 89 → 4005
   - Calculate the sum from 1 to 12 → 78

🧪 DRY RUN MODE - Skipping actual training
✅ Setup complete! Everything looks good.
```

### Run Training

```bash
# Train with default settings
python train_agent.py

# Train with custom parameters
python train_agent.py --iterations 20 --train-size 50 --val-size 20

# Use different algorithm
python train_agent.py --algorithm sft
```

**Command line options:**
- `--dry-run` - Test setup without running training
- `--iterations N` - Number of training iterations (default: 10)
- `--train-size N` - Training dataset size (default: 20)
- `--val-size N` - Validation dataset size (default: 10)
- `--algorithm {apo,sft,rl}` - Training algorithm (default: apo)

## 📊 How It Works

### 1. Architecture

```
train_agent.py
    ↓
    ├── Setup OTLP Exporter → Send traces to Agent Lightning
    ├── Generate Datasets → Math tasks
    ├── Create Trainer → APO/SFT/RL algorithm
    └── Run Training Loop
            ↓
            ├── @rollout function → Run agent on task
            ├── Calculate Reward → Grade response
            └── Send to Algorithm → Improve prompts
```

### 2. Training Flow

1. **Initialize:** Setup OTLP, database, datasets
2. **Rollout:** Run agent with current prompt template
3. **Grade:** Calculate reward for agent response
4. **Learn:** Algorithm improves prompt based on rewards
5. **Repeat:** Continue for N iterations

### 3. Reward Grading

Rewards are calculated based on:
- **Exact match:** 1.0 if answer is correct
- **Partial credit:** 0.5-1.0 based on proximity
- **Wrong answer:** 0.0

## 🎯 Customization

### Add Custom Tasks

Edit `dataset_generator.py`:

```python
def generate_custom_dataset(size: int) -> List[MathTask]:
    """Your custom task generator."""
    tasks = []
    for i in range(size):
        task = MathTask(
            question="Your question",
            expected_answer=42,
            task_id=f"custom_{i}",
            difficulty="medium"
        )
        tasks.append(task)
    return tasks
```

### Modify Reward Logic

Edit `reward_grader.py`:

```python
def calculate_reward(agent_response, expected_answer, **kwargs):
    """Customize reward calculation."""
    # Your custom logic here
    return reward
```

### Change Initial Prompt

Edit `training.py`:

```python
def get_initial_prompt() -> str:
    return """Your custom prompt template here."""
```

## 🔍 Monitoring

### OpenTelemetry Traces

Traces are sent to: `http://localhost:4318/v1/traces`

To view traces, setup a collector (optional):

```bash
# Using Jaeger
docker run -d \
  -p 4318:4318 \
  -p 16686:16686 \
  jaegertracing/all-in-one:latest

# View traces
open http://localhost:16686
```

### Training Database

Training data is saved to: `agno_memory_training.db/`

## ⚠️ Troubleshooting

### ModuleNotFoundError: opentelemetry

```bash
pip install opentelemetry-api opentelemetry-sdk
```

### ModuleNotFoundError: agentlightning

```bash
pip install agentlightning>=0.3.0
```

### OTLP Connection Failed

This is OK if you don't have a collector running. Training will continue.

### Agent API Key Error

Make sure `.env` file has:
```
OPENAI_API_KEY=your_key_here
```

## 📚 References

- [Agent Lightning Docs](https://microsoft.github.io/agent-lightning/)
- [Agno Docs](https://docs.agno.ai/)
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)

## 🎓 Next Steps

1. **Run dry-run** to verify setup
2. **Start training** with small dataset
3. **Monitor results** in training database
4. **Adjust parameters** based on performance
5. **Scale up** to larger datasets

Happy training! 🚀
