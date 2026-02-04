#!/usr/bin/env python
"""Conversation to dataset converter module."""

import logging
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .conversation_extractor import SessionData
from .dataset import TrainingTask

logger = logging.getLogger(__name__)


@dataclass
class ConversationTask:
    """Task extracted from conversation."""
    question: str
    expected_answer: str
    task_id: str
    difficulty: str
    source: str
    session_id: str
    timestamp: Optional[str] = None
    user_id: Optional[str] = None


def convert_session_to_tasks(session: SessionData) -> List[ConversationTask]:
    """
    Convert a session to training tasks, handling tool calls.
    """
    tasks = []
    messages = session.messages
    
    i = 0
    while i < len(messages):
        msg = messages[i]
        
        if msg.get('role') == 'user':
            question = (msg.get('content') or '').strip()
            
            # Find the final assistant response for this question
            answer = ""
            current_idx = i + 1
            last_assistant_idx = -1
            
            # Look ahead until the next user message
            while current_idx < len(messages) and messages[current_idx].get('role') != 'user':
                if messages[current_idx].get('role') == 'assistant':
                    content = (messages[current_idx].get('content') or '').strip()
                    if content:
                        answer = content
                        last_assistant_idx = current_idx
                current_idx += 1
            
            if question and answer:
                # Use the full response content as the ground truth
                expected_answer = answer
                difficulty = estimate_difficulty(question, answer)
                
                task = ConversationTask(
                    question=question,
                    expected_answer=expected_answer,
                    task_id=f"real_{session.session_id}_msg_{i}",
                    difficulty=difficulty,
                    source="real_user_data",
                    session_id=session.session_id,
                    timestamp=session.created_at,
                    user_id=session.user_id
                )
                
                if validate_task_quality(task):
                    tasks.append(task)
                else:
                    logger.info(f"Task rejected by quality validator: {task.task_id}")
            
            # Move to the next potential question
            i = current_idx if current_idx > i else i + 1
        else:
            i += 1
    
    logger.info(f"Converted session {session.session_id} to {len(tasks)} tasks")
    return tasks


def extract_question_answer_pairs(messages: List[Dict[str, Any]]) -> List[tuple]:
    """
    Extract question-answer pairs from messages.
    
    Args:
        messages: List of message dictionaries
        
    Returns:
        List of (question, answer) tuples
    """
    pairs = []
    
    for i in range(len(messages) - 1):
        if messages[i].get('role') == 'user' and messages[i + 1].get('role') == 'assistant':
            question = (messages[i].get('content') or '').strip()
            answer = (messages[i + 1].get('content') or '').strip()
            
            if question and answer:
                pairs.append((question, answer))
    
    return pairs


def extract_answer(response: str) -> str:
    """
    Extract the answer from assistant response.
    
    This tries to find numerical answers, specific values, or
    returns the full response if no clear answer is found.
    
    Args:
        response: Assistant response text
        
    Returns:
        Extracted answer string
    """
    # 1. Look for explicit answer keywords (Highly specific)
    answer_keywords = [
        r'(?:là|=|:|answer is|result is|đáp án là|kết quả là)\s*\**([+-]?[\d,]+(?:\.\d+)?)\**',
        r'([+-]?[\d,]+(?:\.\d+)?)\s*(?:là|is the answer|is the result)'
    ]
    
    for pattern in answer_keywords:
        match = re.search(pattern, response, re.IGNORECASE)
        if match:
            # Clean up commas if any
            return match.group(1).replace(',', '')
    
    # 2. Look for numbers at the very end of the response (Common for assistant responses)
    end_match = re.search(r'([+-]?[\d,]+(?:\.\d+)?)\s*[\.\!]*$', response)
    if end_match:
        return end_match.group(1).replace(',', '')
    
    # 3. Look for bolded numbers (Common in Markdown)
    bold_match = re.search(r'\*\*([+-]?[\d,]+(?:\.\d+)?)\*\*', response)
    if bold_match:
        return bold_match.group(1).replace(',', '')
    
    # 4. Fallback search (Broadest)
    # Try to find final answer patterns
    final_answer_patterns = [
        r'(?:kết quả|đáp án|answer|result)(?:\s+là|\s+is|\s*:)\s*(.+?)(?:\.|$)',
        r'(?:vậy|therefore|thus|so)\s+(.+?)(?:\.|$)'
    ]
    
    for pattern in final_answer_patterns:
        match = re.search(pattern, response, re.IGNORECASE)
        if match:
            answer = match.group(1).strip()
            answer = re.sub(r'\s+', ' ', answer)
            return answer[:100]
    
    # 5. Last resort: first number or first sentence
    first_num = re.search(r'([+-]?[\d,]+(?:\.\d+)?)', response)
    if first_num:
        return first_num.group(1).replace(',', '')
    
    return response[:100].strip()


def estimate_difficulty(question: str, answer: str) -> str:
    """
    Estimate task difficulty based on question and answer.
    
    Args:
        question: Question text
        answer: Answer text
        
    Returns:
        Difficulty level: "easy", "medium", or "hard"
    """
    # Simple heuristics for difficulty
    question_length = len(question)
    answer_length = len(answer)
    
    # Check for mathematical complexity
    has_large_numbers = bool(re.search(r'\b\d{3,}\b', question))
    has_multiple_operations = question.count('+') + question.count('-') + \
                             question.count('*') + question.count('/') > 1
    
    # Difficulty rules
    if question_length < 50 and answer_length < 50 and not has_large_numbers:
        return "easy"
    elif has_large_numbers or has_multiple_operations or question_length > 150:
        return "hard"
    else:
        return "medium"


def validate_task_quality(task: ConversationTask) -> bool:
    """
    Validate if a task meets quality criteria.
    
    Quality criteria:
    - Question is not too short or too long
    - Answer is meaningful
    - No obvious errors or placeholders
    
    Args:
        task: ConversationTask to validate
        
    Returns:
        True if task passes quality checks
    """
    # Check question length
    if len(task.question) < 10:
        logger.debug(f"Rejected: Question too short ({len(task.question)} chars) - '{task.question}'")
        return False
    
    if len(task.question) > 500:
        logger.debug(f"Rejected: Question too long ({len(task.question)} chars)")
        return False
    
    # Check answer is not empty
    if len(task.expected_answer) < 1:
        logger.debug("Rejected: Empty answer")
        return False
    
    # Check for error indicators
    error_keywords = ['error', 'lỗi', 'failed', 'thất bại', 'không thể', 'cannot']
    question_lower = task.question.lower()
    answer_lower = task.expected_answer.lower()
    
    for keyword in error_keywords:
        if keyword in question_lower or keyword in answer_lower:
            logger.debug(f"Rejected: Contains error keyword '{keyword}'")
            return False
    
    # Check for placeholders
    placeholder_keywords = ['placeholder', 'example', 'ví dụ', 'todo', 'xxx']
    for keyword in placeholder_keywords:
        if keyword in question_lower or keyword in answer_lower:
            logger.debug(f"Rejected: Contains placeholder '{keyword}'")
            return False
    
    return True


def convert_to_training_task(task: ConversationTask) -> TrainingTask:
    """
    Convert ConversationTask to TrainingTask format for compatibility.
    
    Args:
        task: ConversationTask to convert
        
    Returns:
        MathTask formatted task
    """
    # Try to parse expected_answer as int
    try:
        expected_int = int(float(task.expected_answer))
    except (ValueError, TypeError):
        # If not a number, use hash of answer
        expected_int = hash(task.expected_answer) % 10000
    
    return TrainingTask(
        question=task.question,
        expected_answer=expected_int,
        task_id=task.task_id,
        difficulty=task.difficulty
    )


def batch_convert_sessions(
    sessions: List[SessionData]
) -> List[ConversationTask]:
    """
    Convert multiple sessions to tasks.
    
    Args:
        sessions: List of SessionData
        
    Returns:
        List of ConversationTask
    """
    all_tasks = []
    
    for session in sessions:
        tasks = convert_session_to_tasks(session)
        all_tasks.extend(tasks)
    
    logger.info(f"Converted {len(sessions)} sessions to {len(all_tasks)} tasks")
    return all_tasks
