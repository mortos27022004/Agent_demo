#!/usr/bin/env python
"""
All-in-one Training Script for Agno Agent using Agent Lightning with VeRL (Volcano/PPO).
This script adapts the training logic to use the VeRL algorithm for weight optimization of local models,
rather than prompt optimization (APO) for API models.
"""

import os
import sys
import json
import time
import uuid
import logging
import argparse
import subprocess
import atexit
import re
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any

from dotenv import load_dotenv

# Load environment variables FIRST before any other code
load_dotenv()

# Third-party imports
try:
    from agno.agent import Agent
    from agno.models.openai import OpenAIChat
    from agno.models.google import Gemini
    from agno.db.json import JsonDb
except ImportError:
    print("❌ Agno is not installed. Please install it using `pip install agno`")
    sys.exit(1)

try:
    import agentlightning as agl
    from agentlightning.algorithm.verl import VERL
    from agentlightning.trainer import Trainer
    from agentlightning.adapter import TraceToMessages
    AGENT_LIGHTNING_AVAILABLE = True
except ImportError:
    AGENT_LIGHTNING_AVAILABLE = False
    print("⚠️ Agent Lightning (or VeRL support) is not installed.")


from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

# OpenTelemetry imports
try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource, SERVICE_NAME
    OTLP_AVAILABLE = True
except ImportError:
    OTLP_AVAILABLE = False


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# --- Prompts ---

INITIAL_TRAINING_PROMPT = """Bạn là một trợ lý AI giúp tôi giải quyết thắc mắc"""

GRADER_AGENT_INSTRUCTIONS = [
    "Evaluate the agent response against the ground truth and return only a numerical score between 0.0 and 1.0."
]

GRADING_PROMPT_TEMPLATE = """
### ROLE
You are an expert evaluator. Grade the AGENT RESPONSE against the USER QUESTION.

### CONTEXT
User Question: {question}
Agent Response: {agent_response}

### GRADING CRITERIA (0.0 to 1.0)
- 1.0: Perfect. The response is accurate, helpful, and completely answers the user's question.
- 0.8-0.9: Correct info but could be more concise or better phrased.
- 0.5-0.7: Partially correct. Got the main idea but missed some details, made minor errors, or didn't fully address all parts of the question.
- 0.0-0.4: Wrong, irrelevant, or fails to address the question.

### OUTPUT FORMAT
Respond with ONLY the numerical score (e.g., "0.8"). No explanation.
"""


# --- Configuration ---

@dataclass
class TrainingConfig:
    """Configuration for training."""
    n_runners: int = 1
    max_iterations: int = 1
    user_data_db_path: str = "agno_memory.db"
    max_real_data_age_days: int = 30
    model_path: str = "Qwen/Qwen2.5-1.5B-Instruct"  # Default small model for local training
    train_batch_size: int = 16
    n_gpus: int = 1
    google_api_key: Optional[str] = None
    grader_model_id: str = "gemini-2.0-flash"


# --- Data Structures & Utilities ---

@dataclass
class SessionData:
    session_id: str
    user_id: str
    messages: List[Dict[str, Any]]
    created_at: Optional[str] = None

@dataclass
class ConversationTask:
    question: str
    task_id: str
    source: str
    session_id: str
    timestamp: Optional[str] = None
    user_id: Optional[str] = None


def setup_otlp_exporter(endpoint: str = "http://localhost:4318/v1/traces", service_name: str = "agno-agent-verl"):
    if not OTLP_AVAILABLE: return None
    try:
        resource = Resource(attributes={SERVICE_NAME: service_name})
        provider = TracerProvider(resource=resource)
        otlp_exporter = OTLPSpanExporter(endpoint=endpoint, timeout=30)
        provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        trace.set_tracer_provider(provider)
        return provider
    except Exception as e:
        logger.warning(f"⚠️ OTLP exporter setup failed: {e}")
        return None

def llm_grade_response(agent_response: str, question: str, google_api_key: str, model_id: str = "gemini-2.0-flash") -> float:
    """Grade agent response using Gemini."""
    grading_prompt = GRADING_PROMPT_TEMPLATE.format(question=question, agent_response=agent_response)
    
    # Initialize Gemini client
    llm_client = Gemini(id=model_id, api_key=google_api_key)
    
    grader_agent = Agent(
        model=llm_client,
        description="You are an expert evaluator for AI responses.",
        instructions=GRADER_AGENT_INSTRUCTIONS,
        markdown=False
    )
    try:
        response = grader_agent.run(grading_prompt)
        content = str(response.content).strip()
        # Extract score using regex
        score_match = re.search(r'([01]?\.\d+)', content)
        if score_match:
            return min(1.0, max(0.0, float(score_match.group(1))))
        if "1.0" in content or "1" == content: return 1.0
        if "0.0" in content or "0" == content: return 0.0
        return 0.0
    except Exception as e:
        logger.error(f"Grading failed: {e}")
        return 0.0

def calculate_reward(agent_response: str, question: str, google_api_key: str) -> float:
    """Calculate reward for agent response."""
    if not google_api_key:
        return 0.5 # Default middle score if no API key
    return llm_grade_response(agent_response, question, google_api_key)

# Reuse extraction logic
def extract_all_sessions(db_path: str) -> List[SessionData]:
    db_file = Path(db_path)
    if not db_file.exists():
        logger.warning(f"Database not found: {db_path}")
        return []
    
    try:
        db = JsonDb(db_path=str(db_path))
        if hasattr(db, 'get_sessions'):
            try:
                raw_sessions = db.get_sessions(session_type="agent")
            except Exception:
                raw_sessions = db.get_sessions()
        else:
            return _read_sessions_from_files(db_path)

        sessions = []
        for raw_session in raw_sessions:
            if isinstance(raw_session, dict):
                session_id = raw_session.get('session_id', '')
                user_id = raw_session.get('user_id', '')
                messages = raw_session.get('messages', [])
                created_at = raw_session.get('created_at')
            else:
                session_id = getattr(raw_session, 'session_id', '')
                user_id = getattr(raw_session, 'user_id', '')
                raw_messages = getattr(raw_session, 'messages', [])
                if not raw_messages and hasattr(raw_session, 'runs'):
                     runs = getattr(raw_session, 'runs', [])
                     for run in runs: raw_messages.extend(run.get('messages', []) if isinstance(run, dict) else getattr(run, 'messages', []))
                
                messages = []
                for m in raw_messages:
                    if hasattr(m, 'model_dump'): messages.append(m.model_dump())
                    elif hasattr(m, 'to_dict'): messages.append(m.to_dict())
                    elif isinstance(m, dict): messages.append(m)
                    else: messages.append({'role': getattr(m, 'role', ''), 'content': getattr(m, 'content', '')})
                created_at = getattr(raw_session, 'created_at', None)

            sessions.append(SessionData(session_id=session_id, user_id=user_id, messages=messages, created_at=str(created_at) if created_at else None))
        return sessions
    except Exception as e:
        logger.error(f"Failed to extract sessions: {e}")
        return []

def _read_sessions_from_files(db_path: str) -> List[SessionData]:
    sessions = []
    db_dir = Path(db_path) if Path(db_path).is_dir() else Path(db_path).parent
    sessions_file = db_dir / "agno_sessions.json"
    if sessions_file.exists():
        try:
            with open(sessions_file, 'r') as f:
                raw_data = json.load(f)
                for item in raw_data:
                    messages = []
                    if 'runs' in item:
                        for run in item['runs']: messages.extend(run.get('messages', []))
                    sessions.append(SessionData(
                        session_id=item.get('session_id', 'unknown'),
                        user_id=item.get('user_id', 'unknown'),
                        messages=messages,
                        created_at=str(item.get('created_at'))
                    ))
            return sessions
        except Exception: pass
    return sessions

def convert_session_to_tasks(session: SessionData) -> List[dict]:
    tasks = []
    messages = session.messages
    i = 0
    while i < len(messages):
        msg = messages[i]
        if msg.get('role') == 'user':
            question = (msg.get('content') or '').strip()
            j = i + 1
            while j < len(messages) and messages[j].get('role') != 'user':
                j += 1
            
            if question:
                tasks.append({
                    "prompt": question,
                    "question": question,
                    "id": f"{session.session_id}_{i}",
                })
            i = j
        else:
            i += 1
    return tasks

def prepare_datasets(training_config: TrainingConfig) -> Tuple[List[dict], List[dict]]:
    """
    Prepare training datasets from real user conversations.
    
    NOTE: We only extract user questions, NOT full conversation traces.
    This is intentional for Verl (Verification via Reinforcement Learning):
    - Verl needs questions as input tasks
    - Agent generates NEW traces during rollout
    - Learns from rewards, not historical behavior
    """
    print(f"📂 Loading data from: {training_config.user_data_db_path}")
    all_sessions = extract_all_sessions(training_config.user_data_db_path)
    
    # Filter recent (omitted deep logic for brevity, just take all for now or simple filter)
    sessions = all_sessions # [s for s in all_sessions if s.messages]
    
    all_tasks = []
    for s in sessions:
        all_tasks.extend(convert_session_to_tasks(s))
        
    if not all_tasks:
        print("❌ No tasks found. Creating dummy data for demonstration/dry-run.")
        all_tasks = [{"prompt": "What is the capital of France?", "id": "dummy_1"}] * 10
    
    # Split
    split = int(len(all_tasks) * 0.9)
    train = all_tasks[:split]
    val = all_tasks[split:]
    if not val: val = train
    
    print(f"✅ Prepared {len(train)} train, {len(val)} val tasks")
    return train, val


# --- VeRL Trainer Setup ---

def setup_verl_trainer(training_config: TrainingConfig) -> Optional[object]:
    if not AGENT_LIGHTNING_AVAILABLE: return None
    
    # default VeRL configuration structure
    # This structure mirrors the one found in agentlightning.algorithm.verl.interface.py
    verl_config = {
        "algorithm": {
            "adv_estimator": "grpo",
            "use_kl_in_reward": False,
        },
        "data": {
            "train_batch_size": training_config.train_batch_size,
            "max_prompt_length": 1024,
            "max_response_length": 1024,
        },
        "actor_rollout_ref": {
            "rollout": {
                "tensor_model_parallel_size": 1,
                "n": 1,  # Number of sequences per prompt
                "log_prob_micro_batch_size_per_gpu": 4,
                "name": "vllm", # Use vLLM for rollout
                "gpu_memory_utilization": 0.5,
            },
            "actor": {
                "ppo_mini_batch_size": 4,
                "ppo_micro_batch_size_per_gpu": 1,
                "optim": {"lr": 1e-6},
                "use_kl_loss": False,
                "fsdp_config": {
                    "param_offload": True,
                    "optimizer_offload": True,
                },
            },
            "ref": {
                "log_prob_micro_batch_size_per_gpu": 4,
                "fsdp_config": {"param_offload": True},
            },
            "model": {
                "path": training_config.model_path,
                "use_remove_padding": True,
                "enable_gradient_checkpointing": True,
            },
        },
        "trainer": {
            "n_gpus_per_node": training_config.n_gpus,
            "val_before_train": False,
            "logger": ["console"],
            "total_epochs": training_config.max_iterations,
        },
    }
    
    print(f"⚙️ Initializing VeRL with model: {training_config.model_path}")
    algo = VERL(config=verl_config)
    
    # Trainer
    trainer = Trainer(algorithm=algo)
    return trainer


def main():
    parser = argparse.ArgumentParser(description="VeRL Training script")
    parser.add_argument("--epochs", type=int, default=1, help="Total training epochs")
    parser.add_argument("--model-path", type=str, default="Qwen/Qwen2.5-1.5B-Instruct", help="HuggingFace model path")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--gpus", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true")
    
    args = parser.parse_args()
    
    # Check for vllm/verl dependencies if not dry run
    if not args.dry_run:
        try:
            import vllm
            import verl
        except ImportError:
             print("⚠️ vllm or verl not installed. VeRL training requires these packages.")
             print("   pip install vllm verl-llm")
             # Proceeding mostly to show structure, but will likely fail if actual run attempted without deps
    
    # Setup OTLP
    setup_otlp_exporter()

    # Data
    db_path = str(Path(__file__).parent / "core" / "agno_memory.db")
    config = TrainingConfig(
        max_iterations=args.epochs,
        model_path=args.model_path,
        train_batch_size=args.batch_size,
        n_gpus=args.gpus,
        user_data_db_path=db_path,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    train_dataset, val_dataset = prepare_datasets(config)
    print(train_dataset)
    print(val_dataset)
    if args.dry_run:
        print("✅ Dry run: Data prepared, config valid. Exiting.")
        return

    # Trainer
    trainer = setup_verl_trainer(config)
    if not trainer: return
    
    print("🔥 Starting Request-Driven RL (VeRL)...")
    try:
        # Note: VeRL algorithm usually handles the rollout loop internally via the specialized runner.
        # It does not typically use the python-side 'agent' rollout function like APO.
        trainer.fit(train_dataset=train_dataset, val_dataset=val_dataset)
        print("\n✅ Training complete!")
    except Exception as e:
        logger.error(f"❌ Training failed: {e}")
        if "AgentLightningTrainer" in str(e) or "store" in str(e):
             print("\n💡 Tip: Ensure Agent Lightning Store is running or correctly configured if using V1 execution.")

if __name__ == "__main__":
    main()
