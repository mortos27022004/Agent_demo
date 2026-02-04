"""
Dataset Generator module.

Module này tạo datasets cho training:
- Math tasks
- Conversation tasks
- Custom tasks
"""

import random
from typing import List, TypedDict


class MathTask(TypedDict):
    """Math task type definition."""
    question: str
    expected_answer: int
    task_id: str
    difficulty: str


def generate_math_dataset(
    size: int,
    min_value: int = 1,
    max_value: int = 100,
    seed: int = 42
) -> List[MathTask]:
    """
    Generate math tasks dataset.
    
    Args:
        size: Number of tasks to generate
        min_value: Minimum value for n
        max_value: Maximum value for n
        seed: Random seed for reproducibility
        
    Returns:
        List of math tasks
    """
    random.seed(seed)
    tasks = []
    
    for i in range(size):
        n = random.randint(min_value, max_value)
        expected = sum(range(1, n + 1))
        
        # Determine difficulty
        if n <= 20:
            difficulty = "easy"
        elif n <= 50:
            difficulty = "medium"
        else:
            difficulty = "hard"
        
        task = MathTask(
            question=f"Calculate the sum from 1 to {n}",
            expected_answer=expected,
            task_id=f"task_{i:04d}",
            difficulty=difficulty
        )
        tasks.append(task)
    
    return tasks


def generate_calculator_dataset(
    size: int,
    operations: List[str] = None,
    seed: int = 42
) -> List[MathTask]:
    """
    Generate calculator tasks dataset.
    
    Args:
        size: Number of tasks to generate
        operations: List of operations to include
        seed: Random seed
        
    Returns:
        List of calculator tasks
    """
    if operations is None:
        operations = ["add", "subtract", "multiply", "divide"]
    
    random.seed(seed)
    tasks = []
    
    for i in range(size):
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        op = random.choice(operations)
        
        # Calculate expected answer
        if op == "add":
            expected = a + b
            question = f"Calculate {a} + {b}"
        elif op == "subtract":
            expected = a - b
            question = f"Calculate {a} - {b}"
        elif op == "multiply":
            expected = a * b
            question = f"Calculate {a} × {b}"
        else:  # divide
            b = max(1, b)  # Avoid division by zero
            expected = a / b
            question = f"Calculate {a} ÷ {b}"
        
        task = MathTask(
            question=question,
            expected_answer=int(expected) if isinstance(expected, int) else expected,
            task_id=f"calc_{i:04d}",
            difficulty="medium"
        )
        tasks.append(task)
    
    return tasks


def split_dataset(
    tasks: List[MathTask],
    train_ratio: float = 0.8
) -> tuple[List[MathTask], List[MathTask]]:
    """
    Split dataset into train and validation sets.
    
    Args:
        tasks: Full dataset
        train_ratio: Ratio of training data
        
    Returns:
        Tuple of (train_dataset, val_dataset)
    """
    split_idx = int(len(tasks) * train_ratio)
    return tasks[:split_idx], tasks[split_idx:]
