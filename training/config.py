from dataclasses import dataclass
from typing import Optional

@dataclass
class TrainingConfig:
    """Configuration for training process."""
    
    # === Agent Lightning Settings ===
    otlp_endpoint: str = "http://localhost:4318/v1/traces"
    agent_id: str = "agno-agent-v1"
    n_runners: int = 8
    max_iterations: int = 10
    
    # === Algorithm Settings ===
    algorithm: str = "apo"
    # learning_rate is removed as it's not used in APO
    
    # === Reward Settings ===
    use_llm_grader: bool = True
    reward_tolerance: float = 0.1
    
    # === Task Settings ===
    task_type: str = "conversation"
    
    # === Real User Data Settings ===
    use_real_data: bool = True
    user_data_db_path: str = "agno_memory.db"
    max_real_data_age_days: int = 30
