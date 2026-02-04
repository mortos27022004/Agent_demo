"""
Reward Grader module.

Module này đánh giá agent responses và tính rewards:
- Exact match grading
- Partial credit grading
- LLM-based grading (optional)
"""

import re
import logging
from typing import Union, Optional

from agno.models.openai import OpenAIChat


logger = logging.getLogger(__name__)


def extract_answer(response_text: str) -> Optional[Union[int, float]]:
    """
    Extract numerical answer from agent response.
    
    Args:
        response_text: Agent's text response
        
    Returns:
        Extracted number or None if not found
    """
    # Try to find numbers in the response
    # Look for patterns like "answer is 5050" or "result: 5050" or just "5050"
    patterns = [
        r'(?:answer|result|sum|total)(?:\s+is|\s*:|\s*=)\s*(-?\d+\.?\d*)',
        r'(?:^|\s)(-?\d+\.?\d*)(?:\s|$)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, response_text.lower())
        if match:
            try:
                num_str = match.group(1)
                # Try int first, then float
                if '.' in num_str:
                    return float(num_str)
                else:
                    return int(num_str)
            except (ValueError, IndexError):
                continue
    
    return None


def calculate_reward(
    agent_response: str,
    expected_answer: Union[int, float],
    tolerance: float = 0.1,
    use_llm_grader: bool = False,
    llm_client: Optional[OpenAIChat] = None
) -> float:
    """
    Calculate reward for agent response.
    
    Strategies:
    1. Exact match: 1.0 if exact, 0.0 otherwise
    2. Partial credit: Based on answer proximity
    3. LLM grader: Use another LLM to grade (if enabled)
    
    Args:
        agent_response: Agent's text response
        expected_answer: Expected correct answer
        tolerance: Tolerance for partial credit (as fraction)
        use_llm_grader: Whether to use LLM for grading
        llm_client: LLM client for grading
        
    Returns:
        Reward value between 0.0 and 1.0
    """
    # Extract answer from response
    extracted = extract_answer(agent_response)
    
    if extracted is None:
        logger.warning(f"Could not extract answer from: {agent_response[:100]}")
        return 0.0
    
    # Exact match
    if abs(extracted - expected_answer) < 1e-6:
        return 1.0
    
    # Partial credit based on closeness
    diff = abs(extracted - expected_answer)
    max_diff = abs(expected_answer * tolerance)
    
    if max_diff > 0 and diff <= max_diff:
        # Linear partial credit
        partial_reward = 1.0 - (diff / max_diff) * 0.5
        return max(0.0, partial_reward)
    
    # If LLM grader is enabled and available
    if use_llm_grader and llm_client is not None:
        return llm_grade_response(agent_response, expected_answer, llm_client)
    
    return 0.0


def llm_grade_response(
    agent_response: str,
    expected_answer: Union[int, float],
    llm_client: OpenAIChat
) -> float:
    """
    Use LLM to grade agent response.
    
    Args:
        agent_response: Agent's response
        expected_answer: Expected answer
        llm_client: LLM client
        
    Returns:
        Reward between 0.0 and 1.0
    """
    grading_prompt = f"""
    Grade the following agent response on a scale from 0.0 to 1.0.
    
    Question: Calculate a sum
    Expected Answer: {expected_answer}
    Agent Response: {agent_response}
    
    Criteria:
    - 1.0: Correct answer with clear explanation
    - 0.7-0.9: Correct answer but unclear explanation
    - 0.3-0.6: Partially correct or close answer
    - 0.0: Completely wrong
    
    Respond with ONLY a number between 0.0 and 1.0.
    """
    
    try:
        # This is a simplified version - in real usage, you'd call the LLM properly
        # For now, returning 0.0 to avoid actual LLM calls
        logger.info("LLM grading not fully implemented yet")
        return 0.0
    except Exception as e:
        logger.error(f"LLM grading failed: {e}")
        return 0.0


def binary_reward(correct: bool) -> float:
    """
    Simple binary reward.
    
    Args:
        correct: Whether the answer is correct
        
    Returns:
        1.0 if correct, 0.0 otherwise
    """
    return 1.0 if correct else 0.0
