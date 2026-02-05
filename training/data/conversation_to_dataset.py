#!/usr/bin/env python
"""Conversation to dataset converter module."""

import logging
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .conversation_extractor import SessionData

logger = logging.getLogger(__name__)


@dataclass
class ConversationTask:
    """Task extracted from conversation."""
    question: str
    task_id: str
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
            
            if question:
                task = ConversationTask(
                    question=question,
                    task_id=f"real_{session.session_id}_msg_{i}",
                    source="real_user_data",
                    session_id=session.session_id,
                    timestamp=session.created_at,
                    user_id=session.user_id
                )
                
                tasks.append(task)
            
            # Move to the next potential question
            i = current_idx if current_idx > i else i + 1
        else:
            i += 1
    
    logger.info(f"Converted session {session.session_id} to {len(tasks)} tasks")
    return tasks


def convert_to_training_task(task: ConversationTask) -> dict:
    """
    Convert ConversationTask to training dict format.
    """
    return {
        "question": task.question,
        "task_id": task.task_id,
    }


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
