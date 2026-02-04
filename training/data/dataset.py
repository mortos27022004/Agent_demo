"""
Dataset type definitions.

This module contains data structure definitions used in training.
"""

from typing import TypedDict


class TrainingTask(TypedDict):
    """Task type definition for training data."""
    question: str
    expected_answer: int
    task_id: str
    difficulty: str
