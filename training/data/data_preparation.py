#!/usr/bin/env python
"""Data preparation module for training datasets."""

import logging
import sys
from typing import List, Tuple

from ..config import TrainingConfig
from .dataset import TrainingTask
from .conversation_extractor import extract_all_sessions, filter_successful_interactions, get_recent_sessions
from .conversation_to_dataset import batch_convert_sessions, convert_to_training_task

logger = logging.getLogger(__name__)


def prepare_datasets(training_config: TrainingConfig) -> Tuple[List[TrainingTask], List[TrainingTask]]:
    """
    Prepare training and validation datasets from real user conversations.
    
    Args:
        training_config: Training configuration
        
    Returns:
        Tuple of (train_dataset, val_dataset)
        
    Raises:
        SystemExit: If no data is available
    """
    print("📝 Preparing real user data...")
    
    # Extract sessions from database
    print(f"📂 Loading from: {training_config.user_data_db_path}")
    
    sessions = get_recent_sessions(
        db_path=training_config.user_data_db_path,
        days=training_config.max_real_data_age_days
    )
    
    if not sessions:
        logger.error("❌ No sessions found in database")
        print("❌ No conversation data available for training")
        sys.exit(1)
    
    print(f"📊 Found {len(sessions)} recent sessions")
    
    # Filter successful interactions
    sessions = filter_successful_interactions(sessions)
    print(f"✅ Filtered to {len(sessions)} successful sessions")
    
    if not sessions:
        logger.error("❌ No successful sessions after filtering")
        print("❌ No successful conversations available for training")
        sys.exit(1)
    
    # Convert sessions to tasks
    conversation_tasks = batch_convert_sessions(
        sessions=sessions
    )
    
    if not conversation_tasks:
        logger.error("❌ No tasks extracted from conversations")
        print("❌ Failed to extract training tasks from conversations")
        sys.exit(1)
    
    # Convert to TrainingTask format for compatibility
    all_tasks = [convert_to_training_task(task) for task in conversation_tasks]
    
    # Split into train/val (ensure at least 1 task in each if possible)
    total_tasks = len(all_tasks)
    split_idx = int(total_tasks * 0.8)
    
    if split_idx == 0 and total_tasks > 0:
        split_idx = 1
    
    train_dataset = all_tasks[:split_idx]
    val_dataset = all_tasks[split_idx:]
    
    # Ensure validation is not empty for small datasets
    if not val_dataset and total_tasks > 0:
        val_dataset = all_tasks
    
    print(f"✅ Prepared {len(train_dataset)} train, {len(val_dataset)} val tasks (real user data)")
    print_dataset_samples(train_dataset, n=3)
    
    return train_dataset, val_dataset


def print_dataset_samples(dataset: List[TrainingTask], n: int = 3):
    """
    Pretty print dataset samples.
    
    Args:
        dataset: Dataset to sample from
        n: Number of samples to print
    """
    print("\n📋 Sample tasks:")
    for task in dataset[:n]:
        print(f"   - {task['question']} → {task['expected_answer']}")
    print()
