#!/usr/bin/env python
"""Trainer factory module for creating and configuring trainers."""

import logging
import sys
from typing import Optional

from agno.db.json import JsonDb
from core.config import AgentConfig
from ..config import TrainingConfig
from .rollout import setup_trainer, get_initial_prompt

logger = logging.getLogger(__name__)


def create_trainer(
    training_config: TrainingConfig,
    agent_config: AgentConfig,
    db: JsonDb,
    store_url: Optional[str] = None
) -> object:
    """
    Create and configure Agent Lightning trainer.
    
    Args:
        training_config: Training configuration
        agent_config: Agent configuration
        db: Database instance
        store_url: Optional external store URL for debugging
        
    Returns:
        Configured Trainer instance
        
    Raises:
        SystemExit: If trainer creation fails
    """
    initial_prompt = get_initial_prompt()
    
    print(f"🎓 Setting up {training_config.algorithm.upper()} trainer...")
    
    trainer = setup_trainer(
        initial_prompt=initial_prompt,
        algorithm_type=training_config.algorithm,
        n_runners=training_config.n_runners,
        config=agent_config,
        db=db,
        training_config=training_config,
        store_url=store_url
    )
    
    if not trainer:
        logger.error("❌ Failed to create trainer")
        sys.exit(1)
    
    print(f"✅ Trainer ready ({training_config.n_runners} workers)\n")
    
    return trainer, initial_prompt
