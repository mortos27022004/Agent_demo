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


def calculate_reward(
    agent_response: str,
    question: str,
    use_llm_grader: bool = True,
    llm_client: Optional[OpenAIChat] = None
) -> float:
    """
    Calculate reward for agent response based on the question quality.
    
    Args:
        agent_response: Agent's text response
        question: The user's original question
        use_llm_grader: Whether to use LLM for grading
        llm_client: LLM client for grading
        
    Returns:
        Reward value between 0.0 and 1.0
    """
    # Use LLM Grader (Primary strategy for reference-free grading)
    if use_llm_grader:
        if llm_client is None:
            import os
            llm_client = OpenAIChat(id="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
            
        return llm_grade_response(agent_response, question, llm_client)
    
    return 0.0


def llm_grade_response(
    agent_response: str,
    question: str,
    llm_client: OpenAIChat
) -> float:
    """
    Use LLM to grade agent response semantically based on the question.
    """
    from core.prompts import GRADING_PROMPT_TEMPLATE
    grading_prompt = GRADING_PROMPT_TEMPLATE.format(
        question=question,
        agent_response=agent_response
    )
    
    from agno.agent import Agent
    from core.prompts import GRADER_AGENT_INSTRUCTIONS
    
    grader_agent = Agent(
        model=llm_client,
        description="You are an expert evaluator for AI responses.",
        instructions=GRADER_AGENT_INSTRUCTIONS,
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
