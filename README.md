# Setup Instructions

## Quick Start

### 1. Create Virtual Environment

```bash
# Using conda (recommended)
conda create -n agno-env python=3.11 -y
conda activate agno-env

# OR using venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Create `.env` file:

```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

### 4. Run Agent

```bash
# Basic demo
python main.py

# With Agent Lightning (if installed)
python agno_lightning_example.py
```

## Files

- `main.py` - Agno agent with memory and tracing
- `requirements.txt` - Python dependencies
- `.env` - API keys (create this)
- `agno_memory.db/` - Session and trace storage

## Features

✅ Agno AI agent framework  
✅ OpenAI GPT-4o-mini model  
✅ Tool execution (calculator, sum)  
✅ Session memory & history  
✅ OpenTelemetry tracing  
✅ Agent Lightning integration (optional)

## Troubleshooting

**Missing API Key:**
```bash
export OPENAI_API_KEY="sk-..."
```

**Import Errors:**
```bash
pip install --upgrade -r requirements.txt
```

**Connection Errors (Agent Lightning):**
- Normal if LightningStore server not running
- Agent still works, just can't send traces
