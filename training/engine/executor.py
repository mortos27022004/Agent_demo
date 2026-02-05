#!/usr/bin/env python
"""Training executor module for running training loops."""

import logging
import sys
from typing import List, Tuple

from agno.db.json import JsonDb
from core.config import AgentConfig
from ..config import TrainingConfig
from .rollout import agno_agent_rollout, setup_trainer, get_initial_prompt

logger = logging.getLogger(__name__)


def run_training(
    training_config: TrainingConfig,
    agent_config: AgentConfig,
    db: JsonDb,
    train_dataset: List[dict],
    val_dataset: List[dict],
    store_url: str = None
) -> Tuple[object, str]:
    """
    Run the complete training cycle: creation + execution.
    
    Returns:
        Tuple of (trainer, initial_prompt)
    """
    # 1. Create trainer
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
    
    # 2. Execute training loop
    print("🔥 Starting training loop...")
    
    try:
        trainer.fit(
            agent=agno_agent_rollout,
            train_dataset=train_dataset,
            val_dataset=val_dataset
        )
        
        print("\n" + "=" * 60)
        print("✅ Training complete!")
        
    except Exception as e:
        logger.error(f"❌ Training failed: {e}", exc_info=True)
        sys.exit(1)
    
    return trainer, initial_prompt
