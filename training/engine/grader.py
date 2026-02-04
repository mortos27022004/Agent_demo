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
    expected_answer: Union[int, float, str],
    tolerance: float = 0.1,
    use_llm_grader: bool = True,
    llm_client: Optional[OpenAIChat] = None
) -> float:
    """
    Calculate reward for agent response.
    
    Strategies:
    1. Numerical match: If both look like numbers, use tolerance.
    2. LLM grader: Use another LLM to grade semantics (default for full text).
    
    Args:
        agent_response: Agent's text response
        expected_answer: Expected correct answer (often full raw response)
        tolerance: Tolerance for partial credit (for numbers)
        use_llm_grader: Whether to use LLM for grading
        llm_client: LLM client for grading
        
    Returns:
        Reward value between 0.0 and 1.0
    """
    # 1. Try numerical comparison first (only if both are strictly numbers)
    try:
        if isinstance(expected_answer, (int, float)) or (isinstance(expected_answer, str) and re.match(r'^[+-]?[\d,]+(?:\.\d+)?$', expected_answer.strip())):
            extracted_num = extract_answer(agent_response)
            expected_num = float(str(expected_answer).replace(',', ''))
            
            if extracted_num is not None:
                if abs(extracted_num - expected_num) < 1e-6:
                    return 1.0
                
                diff = abs(extracted_num - expected_num)
                max_diff = abs(expected_num * tolerance)
                if max_diff > 0 and diff <= max_diff:
                    return max(0.0, 1.0 - (diff / max_diff) * 0.5)
    except (ValueError, TypeError):
        pass

    # 2. Use LLM Grader for everything else (Semantic similarity)
    if use_llm_grader:
        if llm_client is None:
            import os
            llm_client = OpenAIChat(id="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
            
        return llm_grade_response(agent_response, str(expected_answer), llm_client)
    
    # 3. Last fallback: basic string match (very strict)
    return 1.0 if agent_response.strip() == str(expected_answer).strip() else 0.0


def llm_grade_response(
    agent_response: str,
    expected_answer: str,
    llm_client: OpenAIChat
) -> float:
    """
    Use LLM to grade agent response semantically compared to ground truth.
    """
    grading_prompt = f"""
    ### ROLE
    You are an expert evaluator. Grade the AGENT RESPONSE against the EXPECTED ANSWER (Ground Truth).
    
    ### CONTEXT
    Expected Answer (Ground Truth): {expected_answer}
    Agent Response: {agent_response}
    
    ### GRADING CRITERIA (0.0 to 1.0)
    - 1.0: Perfect. Matches the meaning, factuality, and intent of the ground truth.
    - 0.8-0.9: Correct info but different phrasing or slightly more/less detail.
    - 0.5-0.7: Partially correct. Got the main idea but missed some details or made minor errors.
    - 0.0-0.4: Wrong or irrelevant.
    
    ### OUTPUT FORMAT
    Respond with ONLY the numerical score (e.g., "0.8"). No explanation.
    """
    
    from agno.agent import Agent
    
    grader_agent = Agent(
        model=llm_client,
        description="You are an expert evaluator for AI responses.",
        instructions=["Evaluate the agent response against the ground truth and return only a numerical score between 0.0 and 1.0."],
        markdown=False
    )
    
    try:
        response = grader_agent.run(grading_prompt)
        content = str(response.content).strip()
        
        # Extract score
        score_match = re.search(r'([01]?\.\d+)', content)
        if score_match:
            return min(1.0, max(0.0, float(score_match.group(1))))
        
        # Fallback for "1" or "0"
        if "1.0" in content or content == "1": return 1.0
        if "0.0" in content or content == "0": return 0.0
        
        logger.warning(f"Could not parse score from content: {content}")
        return 0.0
    except Exception:
        logger.exception("LLM grading failed due to unexpected error")
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
