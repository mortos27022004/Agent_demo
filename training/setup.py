#!/usr/bin/env python
"""Setup module for training dependencies and configuration."""

import logging
import sys
from typing import Tuple

from agno.db.json import JsonDb
from core.config import AgentConfig
from .config import TrainingConfig
from .engine.rollout import AGENT_LIGHTNING_AVAILABLE
from .utils.infrastructure import setup_infrastructure

logger = logging.getLogger(__name__)


def initialize_training(
    iterations: int,
    algorithm: str,
    real_data_db: str = None
) -> Tuple[AgentConfig, TrainingConfig, JsonDb]:
    """
    Consolidated initialization of dependencies, configs, and infrastructure.
    
    Args:
        iterations: Number of training iterations
        algorithm: Training algorithm
        real_data_db: Optional path to real data database
        
    Returns:
        Tuple of (agent_config, training_config, db)
    """
    # 1. Dependency check
    if not AGENT_LIGHTNING_AVAILABLE:
        logger.error("❌ Agent Lightning not installed!")
        logger.error("   Run: pip install agentlightning>=0.3.0")
        sys.exit(1)
    print("✅ Agent Lightning available")
    
    # 2. Config setup
    agent_config = AgentConfig()
    training_config = TrainingConfig(
        max_iterations=iterations,
        algorithm=algorithm
    )
    if real_data_db:
        training_config.user_data_db_path = real_data_db
        
    print(f"📊 Configuration: {training_config.algorithm.upper()}, {training_config.max_iterations} iterations")
    
    # 3. Infrastructure setup
    db = setup_infrastructure(training_config)

    return agent_config, training_config, db
