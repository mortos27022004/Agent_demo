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
    
    # === Training Dataset ===
    train_size: int = 20
    val_size: int = 10
    
    # === Algorithm Settings ===
    algorithm: Literal["apo", "sft", "rl"] = "apo"
    learning_rate: float = 0.001
    
    # === Reward Settings ===
    use_llm_grader: bool = False
    reward_tolerance: float = 0.1  # 10% tolerance for partial credit
    
    # === Task Settings ===
    task_type: Literal["math", "conversation", "custom"] = "math"
    min_task_value: int = 1
    max_task_value: int = 100


# Default configuration instance
default_config = TrainingConfig()
