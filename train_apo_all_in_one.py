#!/usr/bin/env python
"""
All-in-one Training Script for Agno Agent using Agent Lightning.
Contains all necessary logic for data preparation, training, and result saving.
"""

import os
import sys
import json
import time
import uuid
import logging
import argparse
import asyncio
import subprocess
import atexit
import re
import time
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any, Union
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from dotenv import load_dotenv
from agno.tools import Function
from core.tools import *
# Load environment variables FIRST before any other code
load_dotenv()

# Third-party imports
# try:
from agno.agent import Agent
from agno.models.google import Gemini
from agno.db.json import JsonDb
# except ImportError:
#     print("❌ Agno is not installed. Please install it using `pip install agno`")
#     sys.exit(1)

try:
    import agentlightning as agl
    from agentlightning.algorithm import APO
    from agentlightning.trainer import Trainer
    from agentlightning.adapter import TraceToMessages
    from agentlightning import LightningStoreClient
    AGENT_LIGHTNING_AVAILABLE = True
except ImportError:
    AGENT_LIGHTNING_AVAILABLE = False
    print("⚠️ Agent Lightning is not installed. Training features will be limited.")

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


# --- Configuration ---

@dataclass
class AgentConfig:
    """Configuration for the Agent."""
    model_id: str = "gemini-2.0-flash"  # Gemini model
    db_filename: str = "agno_memory.db"
    db_path: Optional[Path] = None
    user_id: str = "user_demo"
    session_id: str = "demo_session"
    num_history_messages: int = 10
    debug_mode: bool = True
    use_best_prompt: bool = True
    fallback_to_default: bool = True
    google_api_key: Optional[str] = None
    tools: list = field(default_factory=lambda: [
        Function.from_callable(sum_1_to_n),
        Function.from_callable(calculator),
        Function.from_callable(get_area_of_circle),
        Function.from_callable(get_area_of_rectangle)
    ])

@dataclass
class TrainingConfig:
    """Configuration for training."""
    n_runners: int = 1
    max_iterations: int = 1
    algorithm: str = "apo"
    user_data_db_path: str = "agno_memory.db"
    max_real_data_age_days: int = 30
    otlp_endpoint: str = "http://localhost:4318/v1/traces"
    agent_id: str = "agno-agent-setup"


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


# --- Data Structures ---

@dataclass
class SessionData:
    """Session data structure."""
    session_id: str
    user_id: str
    messages: List[Dict[str, Any]]
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class ConversationTask:
    """Task extracted from conversation."""
    question: str
    task_id: str
    source: str
    session_id: str
    timestamp: Optional[str] = None
    user_id: Optional[str] = None

@dataclass
class PromptRecord:
    """Record of a trained prompt with metadata."""
    id: str
    prompt_text: str
    timestamp: str
    training_reward: float
    iteration: int
    algorithm: str
    is_active: bool = False
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    def to_dict(self):
        return asdict(self)


# --- Utilities ---

def setup_otlp_exporter(endpoint: str = "http://localhost:4318/v1/traces", service_name: str = "agno-agent") -> Optional[Any]:
    """Setup OTLP exporter for Agent Lightning."""
    if not OTLP_AVAILABLE:
        return None
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

_store_process = None

def cleanup_store():
    """Cleanup store server on exit."""
    global _store_process
    if _store_process:
        print("\n🛑 Shutting down store server...")
        _store_process.terminate()
        try:
            _store_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            _store_process.kill()
        _store_process = None

def start_store_server(store_url: str = None) -> bool:
    """Start store server in background."""
    global _store_process
    if not store_url: return True
    
    os.environ["AGL_MANAGED_STORE"] = "false"
    try:
        port = int(store_url.split(":")[-1])
    except (ValueError, IndexError):
        port = 4747
    
    print(f"🚀 Starting store server on port {port}...")
    _store_process = subprocess.Popen(
        ["agl", "store", "--port", str(port)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    atexit.register(cleanup_store)
    print("⏳ Waiting for store server to start...")
    time.sleep(5)  # Increased wait time for server startup
    
    if _store_process.poll() is not None:
        stdout, stderr = _store_process.communicate()
        print(f"❌ Store server failed to start:\n{stderr}")
        return False
    
    print(f"✅ Store server running (PID: {_store_process.pid})")
    print(f"🔗 Using external store: {store_url}")
    return True


class PromptManager:
    """Manager for best prompt persistence."""
    def __init__(self, storage_path: Optional[Path] = None):
        if storage_path is None:
            storage_path = Path(__file__).parent / "best_prompts.json"
        self.storage_path = Path(storage_path)
        if not self.storage_path.exists() or self.storage_path.stat().st_size == 0:
            self._init_storage()
    
    def _init_storage(self):
        with open(self.storage_path, 'w') as f:
            json.dump({"version": "1.0", "prompts": []}, f)
    
    def _read_storage(self) -> dict:
        try:
            if self.storage_path.stat().st_size == 0: return {"version": "1.0", "prompts": []}
            with open(self.storage_path, 'r') as f: return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"version": "1.0", "prompts": []}
    
    def _write_storage(self, data: dict):
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def save_prompt(self, prompt_text: str, training_reward: float, iteration: int, algorithm: str = "apo", metadata: dict = None, set_active: bool = True) -> PromptRecord:
        data = self._read_storage()
        record = PromptRecord(
            id=str(uuid.uuid4()), prompt_text=prompt_text, timestamp=datetime.now().isoformat(),
            training_reward=training_reward, iteration=iteration, algorithm=algorithm,
            is_active=set_active, metadata=metadata or {}
        )
        if set_active:
            for prompt in data["prompts"]: prompt["is_active"] = False
        data["prompts"].append(record.to_dict())
        self._write_storage(data)
        logger.info(f"✅ Saved prompt (ID: {record.id[:8]}..., Reward: {record.training_reward:.3f})")
        return record


# --- Data Extraction & Preparation ---

def extract_all_sessions(db_path: str) -> List[SessionData]:
    db_file = Path(db_path)
    if not db_file.exists():
        logger.warning(f"Database not found: {db_path}")
        return []
    
    try:
        # Simplified extraction logic reading directly from JSON if possible, else using JsonDb
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
            # Handle both dict and object
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

def filter_sessions_by_date(sessions: List[SessionData], start_date: Optional[datetime], end_date: Optional[datetime] = None) -> List[SessionData]:
    filtered = []
    for session in sessions:
        if not session.created_at:
            filtered.append(session)
            continue
        try:
            if isinstance(session.created_at, (int, float)): session_date = datetime.fromtimestamp(session.created_at)
            elif isinstance(session.created_at, str) and session.created_at.replace('.', '').isdigit(): session_date = datetime.fromtimestamp(float(session.created_at))
            else: session_date = datetime.fromisoformat(session.created_at)
            
            if start_date and session_date < start_date: continue
            if end_date and session_date > end_date: continue
            filtered.append(session)
        except Exception: continue
    return filtered

def filter_successful_interactions(sessions: List[SessionData]) -> List[SessionData]:
    filtered = []
    for session in sessions:
        has_user, has_assistant, has_error = False, False, False
        for msg in session.messages:
            role = msg.get('role', '')
            content = msg.get('content', '')
            if role == 'user': has_user = True
            elif role == 'assistant': has_assistant = True
            if content and isinstance(content, str) and ('error' in content.lower() or 'failed' in content.lower()): has_error = True
        if has_user and has_assistant and not has_error: filtered.append(session)
    return filtered

def convert_session_to_tasks(session: SessionData) -> List[ConversationTask]:
    tasks = []
    messages = session.messages
    i = 0
    while i < len(messages):
        msg = messages[i]
        if msg.get('role') == 'user':
            question = (msg.get('content') or '').strip()
            current_idx = i + 1
            while current_idx < len(messages) and messages[current_idx].get('role') != 'user':
                current_idx += 1
            if question:
                tasks.append(ConversationTask(
                    question=question,
                    task_id=f"real_{session.session_id}_msg_{i}",
                    source="real_user_data",
                    session_id=session.session_id,
                    timestamp=session.created_at,
                    user_id=session.user_id
                ))
            i = current_idx if current_idx > i else i + 1
        else:
            i += 1
    return tasks

def prepare_datasets(training_config: TrainingConfig) -> Tuple[List[dict], List[dict]]:
    """
    Prepare training datasets from real user conversations.
    
    NOTE: We only extract user questions, NOT full conversation traces.
    This is intentional for APO (Automatic Prompt Optimization):
    - APO needs questions as input tasks
    - Agent will generate NEW traces during rollout with different prompts
    - APO learns by comparing rewards of these new traces
    - This is prompt optimization, not behavior cloning
    
    If you need to learn from historical traces (behavior cloning),
    use supervised fine-tuning or DPO instead of APO.
    """
    print("📝 Preparing real user data...")
    print(f"📂 Loading from: {training_config.user_data_db_path}")
    
    all_sessions = extract_all_sessions(training_config.user_data_db_path)
    if not all_sessions:
        logger.error("❌ No sessions found")
        sys.exit(1)
        
    cutoff_date = datetime.now() - timedelta(days=training_config.max_real_data_age_days)
    sessions = filter_sessions_by_date(all_sessions, start_date=cutoff_date)
    print(f"📊 Found {len(sessions)} recent sessions")
    
    sessions = filter_successful_interactions(sessions)
    print(f"✅ Filtered to {len(sessions)} successful sessions")
    
    if not sessions:
        logger.error("❌ No successful sessions after filtering")
        sys.exit(1)
    
    all_tasks = []
    for session in sessions:
        for task in convert_session_to_tasks(session):
            all_tasks.append({"question": task.question, "task_id": task.task_id})
            
    if not all_tasks:
        logger.error("❌ No tasks extracted")
        sys.exit(1)
        
    split_idx = int(len(all_tasks) * 0.8)
    if split_idx == 0 and len(all_tasks) > 0: split_idx = 1
    
    train_dataset = all_tasks[:split_idx]
    val_dataset = all_tasks[split_idx:]
    if not val_dataset and len(all_tasks) > 0: val_dataset = all_tasks
    
    print(f"✅ Prepared {len(train_dataset)} train, {len(val_dataset)} val tasks")
    print(f"\n📋 Sample task: {train_dataset if train_dataset else 'None'}\n")
    
    return train_dataset, val_dataset


# --- Grading & Rollout ---

def llm_grade_response(agent_response: str, question: str, llm_client: Gemini) -> float:
    grading_prompt = GRADING_PROMPT_TEMPLATE.format(question=question, agent_response=agent_response)
    grader_agent = Agent(
        model=llm_client,
        description="You are an expert evaluator for AI responses.",
        instructions=GRADER_AGENT_INSTRUCTIONS,
        markdown=False
    )
    try:
        response = grader_agent.run(grading_prompt)
        content = str(response.content).strip()
        score_match = re.search(r'([01]?\.\d+)', content)
        if score_match: return min(1.0, max(0.0, float(score_match.group(1))))
        if "1.0" in content or "1" == content: return 1.0
        if "0.0" in content or "0" == content: return 0.0
        return 0.0
    except Exception:
        return 0.0

def calculate_reward(agent_response: str, question: str, llm_client: Optional[Gemini] = None) -> float:
    """Calculate reward for agent response.
    
    Returns fixed reward to avoid rate limiting from grader API calls.
    Set ENABLE_LLM_GRADER=true in .env to enable LLM grading.
    """
    if llm_client is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        llm_client = Gemini(
            id="gemini-2.0-flash",
            api_key=api_key
        )
    return llm_grade_response(agent_response, question, llm_client)


def create_agent_with_prompt(prompt_template: str, config: AgentConfig, db: JsonDb) -> Agent:
    instructions = [line.strip() for line in prompt_template.strip().split('\\n') if line.strip()]
    tools = getattr(config, 'tools', [])
    agent = Agent(
        model=Gemini(id=config.model_id, api_key=config.google_api_key),
        tools=tools, instructions=instructions, db=db,
        user_id=config.user_id, session_id=config.session_id,
        add_history_to_context=False, markdown=True, debug_mode=False
    )
    return agent


@agl.rollout
def agno_agent_rollout(task: dict, prompt_template: agl.PromptTemplate, **resources) -> float:
    config = resources.get("config") or AgentConfig()
    db = resources.get("db")
    training_config = resources.get("training_config") or TrainingConfig()
    
    # Wait BEFORE API call to avoid rate limiting
    time.sleep(6)
    
    agent = create_agent_with_prompt(str(prompt_template), config, db)
    
    try:
        response = agent.run(task["question"])
        reward = calculate_reward(response.content, task["question"])
        logger.info(f"Task {task['task_id']}: Q='{task['question'][:30]}...', Reward={reward:.2f}")
        return reward
    except Exception as e:
        logger.error(f"Error in rollout: {e}")
        return 0.0


def setup_trainer(initial_prompt: str, algorithm_type: str, n_runners: int, config: AgentConfig, db: JsonDb, training_config: TrainingConfig, store_url: str) -> Optional[object]:
    if not AGENT_LIGHTNING_AVAILABLE: return None
    
    from openai import AsyncOpenAI
    # Get configuration for Google Gemini OpenAI-compatible API
    api_key = os.getenv("GOOGLE_API_KEY")
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

    async_client = AsyncOpenAI(api_key=api_key, base_url=base_url)
    
    if algorithm_type == "apo":
        algo = APO(
            async_openai_client=async_client,
            gradient_model="gemini-2.0-flash", 
            apply_edit_model="gemini-2.0-flash",
            beam_width=1,  # Reduced from 2 to avoid rate limits
            branch_factor=1,
            beam_rounds=1,
            gradient_batch_size=1,  # Reduced from 4 to avoid rate limits
            val_batch_size=1,  # Reduced from 8 to avoid rate limits
            diversity_temperature=1.0,
            rollout_batch_timeout=3600.0,
            run_initial_validation=True
        )
    
    prompt_resource = agl.PromptTemplate(template=initial_prompt, engine="f-string")
    resources = {"main_prompt": prompt_resource, "config": config, "db": db, "training_config": training_config}
    
    store = None
    if store_url:
        try:
            store = LightningStoreClient(store_url)
            logger.info(f"✅ Connected to external store: {store_url}")
        except Exception: pass
        
    trainer = Trainer(algorithm=algo, n_runners=n_runners, initial_resources=resources, adapter=TraceToMessages(), store=store)
    # Store async_client reference for cleanup
    trainer._async_client = async_client
    return trainer


def save_training_results(trainer, initial_prompt: str, training_config: TrainingConfig):
    print("\n💾 Saving best prompt...")
    best_prompt = initial_prompt
    best_reward = 0.0
    
    if hasattr(trainer.algorithm, 'get_best_prompt'):
        try:
            best_prompt = str(trainer.algorithm.get_best_prompt())
            if hasattr(trainer.algorithm, '_history_best_score'):
                best_reward = trainer.algorithm._history_best_score
        except Exception: pass
    
    pm = PromptManager()
    record = pm.save_prompt(
        prompt_text=best_prompt, training_reward=best_reward,
        iteration=training_config.max_iterations, algorithm=training_config.algorithm
    )
    print(f"✅ Saved prompt (ID: {record.id[:8]}..., Reward: {best_reward:.2f})")


# --- Main ---

def get_agent_config() -> AgentConfig:
    api_key = os.getenv("GOOGLE_API_KEY")
    return AgentConfig(
        model_id="gemini-2.0-flash",
        db_filename="agno_memory.db",
        google_api_key=api_key
    )

def main():
    parser = argparse.ArgumentParser(description="All-in-one Agno Training")
    parser.add_argument("--iterations", type=int, default=1)
    parser.add_argument("--algorithm", type=str, default="apo")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--store-url", type=str, default="http://localhost:4747")
    parser.add_argument("--real-data-db", type=str, default="agno_memory.db")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    # Setup Infrastructure
    print("\nAttempting to start store server...")
    start_store_server(args.store_url)

    # OTLP
    print("🔧 Setting up OTLP exporter...")
    # setup_otlp_exporter()

    # DB
    print("💾 Setting up database...")
    db_path = Path(__file__).parent / "utils" / "agno_memory_training.db"
    db = JsonDb(db_path=str(db_path))

    # Config
    agent_config = get_agent_config()
    real_db_path = str(Path(__file__).parent / "core" / "agno_memory.db")
    training_config = TrainingConfig(
        n_runners=args.workers, 
        max_iterations=args.iterations, 
        algorithm=args.algorithm,
        user_data_db_path=real_db_path
    )
    
    # Data
    if args.dry_run:
        print("Dry run: Skipping data loading and training.")
        return

    try:
        train_dataset, val_dataset = prepare_datasets(training_config)
    except SystemExit:
        return

    # Trainer & Execution
    initial_prompt = INITIAL_TRAINING_PROMPT
    print(f"🎓 Setting up {training_config.algorithm.upper()} trainer...")
    trainer = setup_trainer(
        initial_prompt, 
        training_config.algorithm, 
        training_config.n_runners, 
        agent_config, 
        db, 
        training_config, 
        args.store_url
    )
    
    print("🔥 Starting training loop...")
    try:
        trainer.fit(
            agent=agno_agent_rollout, 
            train_dataset=train_dataset, 
            val_dataset=val_dataset
        )
        print("\n✅ Training complete!")
        save_training_results(trainer, initial_prompt, training_config)
    except KeyboardInterrupt:
        logger.info("⚠️ Training interrupted by user")
    except Exception as e:
        logger.error(f"❌ Training failed: {e}", exc_info=True)
    finally:
        # Cleanup async resources
        print("\n🧹 Cleaning up resources...")
        async_client = None
        
        # Try to get async client from trainer or algorithm
        try:
            if hasattr(trainer, '_async_client'):
                async_client = trainer._async_client
            elif hasattr(trainer, 'algorithm') and hasattr(trainer.algorithm, '_async_client'):
                async_client = trainer.algorithm._async_client
            
            # Close the async client properly
            if async_client and hasattr(async_client, 'close'):
                # Use asyncio.run to properly close in isolated event loop
                try:
                    # Get or create event loop
                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            # If loop is running, create a new one
                            raise RuntimeError("Loop is running")
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                    
                    # Close the client
                    loop.run_until_complete(async_client.close())
                    logger.info("✅ Async client closed successfully")
                except Exception as close_error:
                    logger.warning(f"Error closing async client: {close_error}")
        except Exception as e:
            logger.warning(f"Cleanup warning: {e}")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
