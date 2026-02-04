"""
Training Configuration module cho Agent Lightning.

Module này chứa cấu hình cho:
- Agent Lightning settings
- Training parameters
- Algorithm configuration
- Dataset sizes
"""

from dataclasses import dataclass
from typing import Literal


@dataclass
class TrainingConfig:
    """Cấu hình cho Agent Lightning training."""
    
    # === Agent Lightning Settings ===
    otlp_endpoint: str = "http://localhost:4318/v1/traces"
    agent_id: str = "agno-agent-v1"
    n_runners: int = 8
    max_iterations: int = 10
    
    # === Algorithm Settings ===
    algorithm: Literal["apo", "sft", "rl"] = "apo"
    learning_rate: float = 0.001
    
    # === Reward Settings ===
    use_llm_grader: bool = True
    reward_tolerance: float = 0.1  # 10% tolerance for partial credit
    
    # === Task Settings ===
    task_type: Literal["math", "conversation", "custom"] = "conversation"
    
    # === Real User Data Settings ===
    use_real_data: bool = True
    user_data_db_path: str = "agno_memory.db"
    max_real_data_age_days: int = 30  # Only use recent data


# Default configuration instance
default_config = TrainingConfig()
