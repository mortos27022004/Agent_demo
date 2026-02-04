#!/usr/bin/env python
"""Conversation extractor module for extracting data from Agno JsonDb."""

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from agno.db.json import JsonDb

logger = logging.getLogger(__name__)


@dataclass
class SessionData:
    """Session data structure."""
    session_id: str
    user_id: str
    messages: List[Dict[str, Any]]
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


def extract_all_sessions(db_path: str) -> List[SessionData]:
    """
    Extract all sessions from Agno database.
    
    Args:
        db_path: Path to JsonDb database file
        
    Returns:
        List of SessionData objects
    """
    logger.info(f"Extracting sessions from: {db_path}")
    
    db_file = Path(db_path)
    if not db_file.exists():
        logger.warning(f"Database not found: {db_path}")
        return []
    
    try:
        db = JsonDb(db_path=str(db_path))
        
        # Get all sessions from database
        # Note: JsonDb stores sessions in JSON format
        # We'll read the session data directly
        sessions = []
        
        # Try to get sessions using Agno's API
        # The exact method depends on Agno version
        if hasattr(db, 'get_sessions'):
            try:
                raw_sessions = db.get_sessions(session_type="agent")
            except Exception as e:
                logger.warning(f"get_sessions(session_type='agent') failed: {e}. Trying without session_type.")
                raw_sessions = db.get_sessions()
                
            for raw_session in raw_sessions:
                if isinstance(raw_session, dict):
                    session_id = raw_session.get('session_id', '')
                    user_id = raw_session.get('user_id', '')
                    messages = raw_session.get('messages', [])
                    created_at = raw_session.get('created_at')
                else:
                    # Handle Agno AgentSession objects
                    session_id = getattr(raw_session, 'session_id', '')
                    user_id = getattr(raw_session, 'user_id', '')
                    raw_messages = getattr(raw_session, 'messages', [])
                    
                    # If messages is empty, try to get from runs
                    if not raw_messages and hasattr(raw_session, 'runs'):
                        runs = getattr(raw_session, 'runs', [])
                        for run in runs:
                            if isinstance(run, dict):
                                raw_messages.extend(run.get('messages', []))
                            else:
                                raw_messages.extend(getattr(run, 'messages', []))
                    
                    # Convert Pydantic Message objects to dicts if necessary
                    messages = []
                    for m in raw_messages:
                        if hasattr(m, 'model_dump'):
                            messages.append(m.model_dump())
                        elif hasattr(m, 'to_dict'):
                            messages.append(m.to_dict())
                        elif not isinstance(m, dict):
                            # Try getattr for common fields if it's some other object
                            messages.append({
                                'role': getattr(m, 'role', ''),
                                'content': getattr(m, 'content', '')
                            })
                        else:
                            messages.append(m)
                            
                    created_at = getattr(raw_session, 'created_at', None)
                
                session = SessionData(
                    session_id=session_id,
                    user_id=user_id,
                    messages=messages,
                    created_at=str(created_at) if created_at else None,
                    updated_at=None,
                    metadata={}
                )
                sessions.append(session)
        else:
            # Fallback: read from JSON files directly
            logger.info("Using direct file reading (Agno API not available)")
            sessions = _read_sessions_from_files(db_path)
        
        logger.info(f"Extracted {len(sessions)} sessions")
        return sessions
        
    except Exception as e:
        logger.error(f"Failed to extract sessions: {e}", exc_info=True)
        return []


def _read_sessions_from_files(db_path: str) -> List[SessionData]:
    """
    Read sessions directly from JSON files.
    
    Args:
        db_path: Path to database directory
        
    Returns:
        List of SessionData
    """
    import json
    
    sessions = []
    db_dir = Path(db_path) if Path(db_path).is_dir() else Path(db_path).parent
    
    # 1. Try reading agno_sessions.json directly (standard for JsonDb)
    sessions_file = db_dir / "agno_sessions.json"
    if sessions_file.exists():
        try:
            with open(sessions_file, 'r') as f:
                raw_data = json.load(f)
                for item in raw_data:
                    # In agno_sessions.json, messages are usually in runs[].messages
                    messages = []
                    if 'runs' in item:
                        for run in item['runs']:
                            messages.extend(run.get('messages', []))
                    
                    session = SessionData(
                        session_id=item.get('session_id', 'unknown'),
                        user_id=item.get('user_id', 'unknown'),
                        messages=messages,
                        created_at=str(item.get('created_at')),
                        updated_at=str(item.get('updated_at')),
                        metadata=item.get('metadata', {})
                    )
                    sessions.append(session)
            return sessions
        except Exception as e:
            logger.warning(f"Failed to read {sessions_file}: {e}")

    # 2. Fallback to searching for individual session files
    session_files = list(db_dir.glob("**/sessions/*.json"))
    
    for session_file in session_files:
        try:
            with open(session_file, 'r') as f:
                data = json.load(f)
                session = SessionData(
                    session_id=data.get('id', session_file.stem),
                    user_id=data.get('user_id', 'unknown'),
                    messages=data.get('messages', []),
                    created_at=str(data.get('created_at')),
                    updated_at=str(data.get('updated_at')),
                    metadata=data.get('metadata', {})
                )
                sessions.append(session)
        except Exception as e:
            logger.warning(f"Failed to read {session_file}: {e}")
            continue
    
    return sessions


def extract_session_conversations(
    session_id: str,
    db: JsonDb
) -> Optional[SessionData]:
    """
    Extract specific session conversations.
    
    Args:
        session_id: Session ID to extract
        db: JsonDb instance
        
    Returns:
        SessionData or None if not found
    """
    try:
        # Try to get session by ID
        if hasattr(db, 'get_session'):
            raw_session = db.get_session(session_id)
            if raw_session:
                return SessionData(
                    session_id=raw_session.get('session_id', session_id),
                    user_id=raw_session.get('user_id', ''),
                    messages=raw_session.get('messages', []),
                    created_at=raw_session.get('created_at'),
                    updated_at=raw_session.get('updated_at'),
                    metadata=raw_session.get('metadata', {})
                )
        
        logger.warning(f"Session {session_id} not found")
        return None
        
    except Exception as e:
        logger.error(f"Failed to extract session {session_id}: {e}")
        return None


def filter_sessions_by_date(
    sessions: List[SessionData],
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[SessionData]:
    """
    Filter sessions by date range.
    
    Args:
        sessions: List of sessions to filter
        start_date: Start date (inclusive)
        end_date: End date (inclusive)
        
    Returns:
        Filtered list of sessions
    """
    filtered = []
    
    for session in sessions:
        if not session.created_at:
            # If no timestamp, include it
            filtered.append(session)
            continue
        
        try:
            if isinstance(session.created_at, (int, float)):
                session_date = datetime.fromtimestamp(session.created_at)
            elif isinstance(session.created_at, str) and session.created_at.replace('.', '').isdigit():
                session_date = datetime.fromtimestamp(float(session.created_at))
            else:
                session_date = datetime.fromisoformat(session.created_at)
            
            if start_date and session_date < start_date:
                continue
            if end_date and session_date > end_date:
                continue
            
            filtered.append(session)
            
        except Exception as e:
            logger.warning(f"Invalid date format for session {session.session_id} ({session.created_at}): {e}")
            continue
    
    logger.info(f"Filtered {len(filtered)}/{len(sessions)} sessions by date")
    return filtered


def filter_successful_interactions(sessions: List[SessionData]) -> List[SessionData]:
    """
    Filter sessions with successful interactions.
    
    A successful interaction has:
    - At least one user message
    - At least one assistant response
    - No error messages
    
    Args:
        sessions: List of sessions to filter
        
    Returns:
        Filtered sessions
    """
    filtered = []
    
    for session in sessions:
        has_user_msg = False
        has_assistant_msg = False
        has_error = False
        
        for msg in session.messages:
            role = msg.get('role', '')
            content = msg.get('content', '')
            
            if role == 'user':
                has_user_msg = True
            elif role == 'assistant':
                has_assistant_msg = True
            
            # Check for error indicators (safe check for None content)
            if content and isinstance(content, str):
                content_lower = content.lower()
                if 'error' in content_lower or 'failed' in content_lower:
                    has_error = True
        
        if has_user_msg and has_assistant_msg and not has_error:
            filtered.append(session)
    
    logger.info(f"Filtered {len(filtered)}/{len(sessions)} successful sessions")
    return filtered


def get_recent_sessions(
    db_path: str,
    days: int = 30
) -> List[SessionData]:
    """
    Get recent sessions from the last N days.
    
    Args:
        db_path: Path to database
        days: Number of days to look back
        
    Returns:
        Recent sessions
    """
    all_sessions = extract_all_sessions(db_path)
    
    if not all_sessions:
        return []
    
    cutoff_date = datetime.now() - timedelta(days=days)
    recent_sessions = filter_sessions_by_date(
        all_sessions,
        start_date=cutoff_date
    )
    
    return recent_sessions


def get_session_statistics(sessions: List[SessionData]) -> Dict[str, Any]:
    """
    Get statistics about sessions.
    
    Args:
        sessions: List of sessions
        
    Returns:
        Statistics dictionary
    """
    total_messages = 0
    total_user_msgs = 0
    total_assistant_msgs = 0
    
    for session in sessions:
        total_messages += len(session.messages)
        for msg in session.messages:
            if msg.get('role') == 'user':
                total_user_msgs += 1
            elif msg.get('role') == 'assistant':
                total_assistant_msgs += 1
    
    return {
        'total_sessions': len(sessions),
        'total_messages': total_messages,
        'total_user_messages': total_user_msgs,
        'total_assistant_messages': total_assistant_msgs,
        'avg_messages_per_session': total_messages / len(sessions) if sessions else 0
    }
