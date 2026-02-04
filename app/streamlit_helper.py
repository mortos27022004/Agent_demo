"""
Helper functions for Streamlit integration.

Module này cung cấp các utility functions để:
- Format messages và responses
- Quản lý session data
- Tính toán analytics
- Visualize agent process
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def format_timestamp(timestamp: Optional[str] = None) -> str:
    """
    Format timestamp thành dạng dễ đọc.
    
    Args:
        timestamp: ISO format timestamp string
        
    Returns:
        Formatted timestamp string
    """
    if timestamp is None:
        return datetime.now().strftime("%H:%M:%S")
    
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime("%H:%M:%S")
    except Exception:
        return timestamp


def extract_tool_calls(response_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract tool calls từ agent response.
    
    Args:
        response_data: Agent response data
        
    Returns:
        List of tool call information
    """
    tool_calls = []
    
    # Check if response has messages with tool calls
    if 'messages' in response_data:
        for msg in response_data['messages']:
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    tool_calls.append({
                        'name': tool_call.function.name,
                        'arguments': tool_call.function.arguments,
                        'id': tool_call.id
                    })
    
    return tool_calls


def get_session_list(db_path: Path) -> List[Dict[str, Any]]:
    """
    Lấy danh sách các sessions từ database.
    
    Args:
        db_path: Path to database directory
        
    Returns:
        List of session information
    """
    sessions = []
    
    try:
        sessions_dir = db_path / "sessions"
        if sessions_dir.exists():
            for session_file in sessions_dir.glob("*.json"):
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        session_data = json.load(f)
                        sessions.append({
                            'id': session_file.stem,
                            'name': session_data.get('name', session_file.stem),
                            'created_at': session_data.get('created_at', ''),
                            'message_count': len(session_data.get('messages', []))
                        })
                except Exception as e:
                    logger.warning(f"Could not load session {session_file}: {e}")
    except Exception as e:
        logger.error(f"Error loading sessions: {e}")
    
    return sorted(sessions, key=lambda x: x.get('created_at', ''), reverse=True)


def get_conversation_history(db_path: Path, session_id: str) -> List[Dict[str, Any]]:
    """
    Lấy lịch sử hội thoại của một session.
    
    Args:
        db_path: Path to database directory
        session_id: Session ID
        
    Returns:
        List of messages
    """
    messages = []
    
    try:
        session_file = db_path / "sessions" / f"{session_id}.json"
        if session_file.exists():
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
                messages = session_data.get('messages', [])
    except Exception as e:
        logger.error(f"Error loading conversation history: {e}")
    
    return messages


def calculate_analytics(db_path: Path) -> Dict[str, Any]:
    """
    Tính toán analytics từ database.
    
    Args:
        db_path: Path to database directory
        
    Returns:
        Analytics data dictionary
    """
    analytics = {
        'total_sessions': 0,
        'total_messages': 0,
        'tool_usage': {},
        'model_usage': {}
    }
    
    try:
        sessions = get_session_list(db_path)
        analytics['total_sessions'] = len(sessions)
        
        for session in sessions:
            messages = get_conversation_history(db_path, session['id'])
            analytics['total_messages'] += len(messages)
            
            # Count tool usage
            for msg in messages:
                if isinstance(msg, dict):
                    if 'tool_calls' in msg and msg['tool_calls']:
                        for tool_call in msg['tool_calls']:
                            tool_name = tool_call.get('function', {}).get('name', 'unknown')
                            analytics['tool_usage'][tool_name] = analytics['tool_usage'].get(tool_name, 0) + 1
    
    except Exception as e:
        logger.error(f"Error calculating analytics: {e}")
    
    return analytics


def format_tool_call_display(tool_name: str, arguments: str, result: Optional[str] = None) -> str:
    """
    Format tool call cho display.
    
    Args:
        tool_name: Tên tool
        arguments: Arguments JSON string
        result: Tool result (optional)
        
    Returns:
        Formatted string
    """
    display = f"🔧 **{tool_name}**\n"
    
    try:
        args_dict = json.loads(arguments) if isinstance(arguments, str) else arguments
        display += f"```json\n{json.dumps(args_dict, indent=2, ensure_ascii=False)}\n```\n"
    except Exception:
        display += f"```\n{arguments}\n```\n"
    
    if result:
        display += f"\n✅ Kết quả: `{result}`"
    
    return display


def export_conversation(messages: List[Dict[str, Any]], session_id: str) -> str:
    """
    Export conversation thành markdown format.
    
    Args:
        messages: List of messages
        session_id: Session ID
        
    Returns:
        Markdown formatted conversation
    """
    export = f"# Conversation Export - {session_id}\n\n"
    export += f"Exported at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    export += "---\n\n"
    
    for i, msg in enumerate(messages, 1):
        if isinstance(msg, dict):
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            
            if role == 'user':
                export += f"## Message {i} - User\n\n{content}\n\n"
            elif role == 'assistant':
                export += f"## Message {i} - Assistant\n\n{content}\n\n"
            
            export += "---\n\n"
    
    return export


def read_log_file(log_path: str = "output.log", max_lines: int = None) -> List[str]:
    """
    Đọc file log.
    
    Args:
        log_path: Path to log file
        max_lines: Maximum lines to read (None = all lines)
        
    Returns:
        List of log lines
    """
    import os
    
    try:
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                if max_lines:
                    return lines[-max_lines:]
                return lines
        return []
    except Exception as e:
        logger.error(f"Error reading log file: {e}")
        return []


def parse_logs_by_cycle(log_lines: List[str]) -> List[Dict[str, Any]]:
    """
    Parse log lines and group by Q&A cycles.
    
    Each cycle is identified by "Agent Run Start" and "Agent Run End" patterns.
    
    Args:
        log_lines: List of log lines
        
    Returns:
        List of cycles, each containing:
        - timestamp: Start timestamp
        - question: User question
        - logs: List of log lines for this cycle
        - run_id: Agent run ID
    """
    cycles = []
    current_cycle = None
    
    for line in log_lines:
        # Detect start of new Q&A cycle
        if "Agent Run Start:" in line or "❓ Câu hỏi" in line:
            # Save previous cycle if exists
            if current_cycle and current_cycle.get('logs'):
                cycles.append(current_cycle)
            
            # Start new cycle
            current_cycle = {
                'timestamp': None,
                'question': None,
                'logs': [],
                'run_id': None
            }
            
            # Extract run ID if present
            if "Agent Run Start:" in line:
                parts = line.split("Agent Run Start:")
                if len(parts) > 1:
                    run_id = parts[1].strip().replace("***", "").strip()
                    current_cycle['run_id'] = run_id
                    
                # Extract timestamp from log line
                if line.strip():
                    # Try to parse timestamp from beginning of line
                    timestamp_match = line.split(" - ")[0] if " - " in line else None
                    if timestamp_match:
                        current_cycle['timestamp'] = timestamp_match.strip()
                        
            # Extract question
            if "❓ Câu hỏi" in line:
                parts = line.split("❓ Câu hỏi")
                if len(parts) > 1:
                    question_text = parts[1].strip()
                    current_cycle['question'] = question_text
                    
                # Use this as timestamp if not already set
                if not current_cycle['timestamp']:
                    timestamp_match = line.split(" - ")[0] if " - " in line else None
                    if timestamp_match:
                        current_cycle['timestamp'] = timestamp_match.strip()
                    else:
                        # Try to extract from line start
                        current_cycle['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add line to current cycle
        if current_cycle is not None:
            current_cycle['logs'].append(line)
    
    # Don't forget the last cycle
    if current_cycle and current_cycle.get('logs'):
        cycles.append(current_cycle)
    
    # Reverse to show newest first
    return list(reversed(cycles))

