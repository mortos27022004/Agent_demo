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

    best_prompt = initial_prompt
    best_reward = 0.0
    
    if not hasattr(trainer, 'algorithm') or trainer.algorithm is None:
        logger.warning("⚠️ No algorithm found in trainer")
        return best_prompt, best_reward

    # Use APO's native get_best_prompt() method (recommended approach)
    if hasattr(trainer.algorithm, 'get_best_prompt'):
        try:
            best_prompt_obj = trainer.algorithm.get_best_prompt()
            best_prompt = str(best_prompt_obj)
            
            # Extract best score from APO's internal tracking
            if hasattr(trainer.algorithm, '_history_best_score'):
                best_reward = trainer.algorithm._history_best_score
                logger.info(f"✅ Extracted best prompt (reward: {best_reward:.2f})")
            else:
                logger.info("✅ Extracted best prompt (no score available)")
                
            return best_prompt, best_reward
            
        except ValueError as e:
            # APO raises ValueError if run() not called or no best prompt found
            logger.warning(f"⚠️ Could not get best prompt from APO: {e}")
        except Exception as e:
            logger.error(f"❌ Error extracting best prompt: {e}")

    # Fallback: try getting from best_resources (legacy)
    if hasattr(trainer.algorithm, 'best_resources'):
        resources = trainer.algorithm.best_resources
        if resources and 'main_prompt' in resources:
            best_prompt = str(resources['main_prompt'])
            logger.info("✅ Extracted prompt from best_resources (legacy)")
        # Also try old key for backwards compatibility during migration
        elif resources and 'prompt_template' in resources:
            best_prompt = str(resources['prompt_template'])
            logger.warning("⚠️ Using legacy 'prompt_template' key (consider updating)")
    
    return best_prompt, best_reward

