"""
Agno Agent Package with Agent Lightning Integration.

Project structure:
- core/: Core agent components
- training/: Agent Lightning training system
- docs/: Documentation
"""

__version__ = "2.0.0"
__author__ = "Agno Team"

# Import core components
from core import AgentConfig, AgnoAgentManager, sum_1_to_n, calculator

# Import training components (optional)
try:
    from training import (
        TrainingConfig,
        generate_math_dataset,
        setup_trainer,
        agno_agent_rollout,
    )
    TRAINING_AVAILABLE = True
except ImportError:
    TRAINING_AVAILABLE = False

__all__ = [
    "AgentConfig",
    "AgnoAgentManager",
    "sum_1_to_n",
    "calculator",
]

if TRAINING_AVAILABLE:
    __all__.extend([
        "TrainingConfig",
        "generate_math_dataset",
        "setup_trainer",
        "agno_agent_rollout",
    ])
