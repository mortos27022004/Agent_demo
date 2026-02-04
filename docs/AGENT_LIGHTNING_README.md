# Agno + Agent Lightning Integration

## Dependencies

```bash
# Install required packages
pip install agent-lightning
pip install opentelemetry-api opentelemetry-sdk
pip install opentelemetry-exporter-otlp-proto-http
```

## Quick Start

### 1. Start Agent Lightning Store

```bash
# Terminal 1: Start LightningStore server
python -m agent_lightning.store.server --port 4318
```

### 2. Run Example

```bash
# Terminal 2: Run integration example
export OPENAI_API_KEY="sk-your-key-here"
python agno_lightning_example.py
```

### 3. Verify Traces

```bash
# Terminal 3: Check traces arrived
curl http://localhost:4318/api/traces | jq
```

## Files

- `agno_lightning_example.py` - Minimal runnable example
- `implementation_plan.md` - Full integration guide (architecture, setup, verification)

## Key Concepts

**Rollout**: Sequence of agent steps for one task, captured as OpenTelemetry spans

**Reward**: Numeric score (0.0-1.0) attached to rollout for training

**Trace**: Complete execution path with timing and metadata

See `implementation_plan.md` for detailed documentation.
