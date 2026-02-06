#!/usr/bin/env python
"""Setup module for training dependencies and configuration."""

import logging
import os
import sys
from pathlib import Path
from typing import Tuple

from agno.db.json import JsonDb
from .engine.rollout import AGENT_LIGHTNING_AVAILABLE
from .utils.infrastructure import setup_infrastructure

logger = logging.getLogger(__name__)


def get_agent_config() -> dict:
    db_filename = "agno_memory.db"
    return {
        "model_id": "gpt-4o-mini",
        "db_filename": db_filename,
        "db_path": Path(__file__).parent / db_filename,
        "user_id": "user_demo",
        "session_id": "demo_session",
        "num_history_messages": 10,
        "debug_mode": True,
        "use_best_prompt": True,
        "fallback_to_default": True,
        "openai_api_key": os.getenv("OPENAI_API_KEY")
    }


def get_training_config(
    iterations: int,
    algorithm: str,
    n_runners: int = None,
    real_data_db: str = None
) -> dict:

    config = {
        # === Agent Lightning Settings ===
        "otlp_endpoint": "http://localhost:4318/v1/traces",
        "agent_id": "agno-agent-v1",
        "n_runners": n_runners if n_runners is not None else 8,
        "max_iterations": iterations,
        
        # === Algorithm Settings ===
        "algorithm": algorithm,
        "learning_rate": 0.001,
        
        # === Reward Settings ===
        "use_llm_grader": True,
        "reward_tolerance": 0.1,  # 10% tolerance for partial credit
        
        # === Task Settings ===
        "task_type": "conversation",
        
        # === Real User Data Settings ===
        "use_real_data": True,
        "user_data_db_path": real_data_db if real_data_db else "agno_memory.db",
        "max_real_data_age_days": 30  # Only use recent data
    }
    
    print(f"📊 Configuration: {config['algorithm'].upper()}, {config['max_iterations']} iterations, {config['n_runners']} workers")
    
    return config



