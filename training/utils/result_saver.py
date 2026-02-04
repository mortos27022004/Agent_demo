#!/usr/bin/env python
"""Result saver module for saving and exporting training results."""

import logging
from typing import Tuple

from ..config import TrainingConfig
from .prompt_manager import PromptManager

logger = logging.getLogger(__name__)


def save_training_results(
    trainer,
    initial_prompt: str,
    training_config: TrainingConfig
):
    """
    Save best prompt and training results.
    
    Args:
        trainer: Agent Lightning trainer instance
        initial_prompt: Initial prompt template
        training_config: Training configuration
    """
    print("\n💾 Saving best prompt...")
    
    try:
        # Extract best prompt
        best_prompt, best_reward = extract_best_prompt(trainer, initial_prompt)
        
        # Save to prompt manager
        pm = PromptManager()
        record = pm.save_prompt(
            prompt_text=best_prompt,
            training_reward=best_reward,
            iteration=training_config.max_iterations,
            algorithm=training_config.algorithm,
            metadata={
                "train_size": getattr(training_config, 'train_size', 'N/A'),
                "val_size": getattr(training_config, 'val_size', 'N/A'),
                "n_runners": getattr(training_config, 'n_runners', 'N/A'),
                "task_type": getattr(training_config, 'task_type', 'N/A')
            },
            set_active=True
        )
        
        print(f"✅ Saved prompt (ID: {record.id[:8]}..., Reward: {best_reward:.2f})")
        
    except Exception as e:
        logger.warning(f"⚠️  Could not save prompt: {e}")


def extract_best_prompt(trainer, initial_prompt: str) -> Tuple[str, float]:
    """
    Extract best prompt from trainer.
    
    Args:
        trainer: Agent Lightning trainer instance
        initial_prompt: Initial prompt as fallback
        
    Returns:
        Tuple of (best_prompt, best_reward)
    """
    best_prompt = initial_prompt
    best_reward = 0.0
    
    if not hasattr(trainer, 'algorithm') or trainer.algorithm is None:
        return best_prompt, best_reward

    # Try 1: Call get_best_prompt() which many algorithms (like APO) implement
    if hasattr(trainer.algorithm, 'get_best_prompt'):
        try:
            best_prompt = str(trainer.algorithm.get_best_prompt())
            # For APO, the best score is in _history_best_score
            if hasattr(trainer.algorithm, '_history_best_score'):
                best_reward = trainer.algorithm._history_best_score
            print("✅ Extracted best prompt via get_best_prompt()")
            return best_prompt, best_reward
        except Exception:
            pass

    # Try 2: Legacy fallback to best_resources
    if hasattr(trainer.algorithm, 'best_resources'):
        resources = trainer.algorithm.best_resources
        if resources and 'prompt_template' in resources:
            best_prompt = str(resources['prompt_template'])
            print("✅ Extracted optimized prompt from best_resources")
    
    return best_prompt, best_reward
