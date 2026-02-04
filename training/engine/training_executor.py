#!/usr/bin/env python
"""Training executor module for running training loops."""

import logging
import sys
from typing import List, Tuple

from agno.db.json import JsonDb
from core.config import AgentConfig
from ..config import TrainingConfig
from ..data.dataset import TrainingTask
from .rollout import agno_agent_rollout
from .trainer_factory import create_trainer

logger = logging.getLogger(__name__)


def run_training(
    training_config: TrainingConfig,
    agent_config: AgentConfig,
    db: JsonDb,
    train_dataset: List[TrainingTask],
    val_dataset: List[TrainingTask],
    store_url: str = None
) -> Tuple[object, str]:
    """
    Run the complete training cycle: creation + execution.
    
    Returns:
        Tuple of (trainer, initial_prompt)
    """
    # 1. Create trainer
    trainer, initial_prompt = create_trainer(
        training_config=training_config,
        agent_config=agent_config,
        db=db,
        store_url=store_url
    )
    
    # 2. Execute training
    execute_training(trainer, train_dataset, val_dataset)
    
    return trainer, initial_prompt


def execute_training(trainer, train_dataset: List[TrainingTask], val_dataset: List[TrainingTask]):
    """
    Execute the training loop.
    
    Args:
        trainer: Agent Lightning trainer instance
        train_dataset: Training dataset
        val_dataset: Validation dataset
        
    Raises:
        SystemExit: If training fails
    """
    print("🔥 Starting training loop...")
    print("=" * 60)
    
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
