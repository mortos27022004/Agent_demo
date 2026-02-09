"""
Configuration module cho Agno Agent.

Module này chứa tất cả cấu hình cho agent, bao gồm:
- Model settings
- Database paths
- User và session IDs
- Debug mode
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

DEFAULT_DB_PATH = Path(__file__).parent / "agno_memory.db"

@dataclass
class AgentConfig:
    """Configuration for the Agent."""
    model_id: str = "gemini-2.0-flash"
    db_filename: str = "agno_memory.db"
    db_path: Optional[Path] = None
    user_id: str = "user_demo"
    session_id: str = "demo_session"
    num_history_messages: int = 10
    debug_mode: bool = True
    use_best_prompt: bool = True
    fallback_to_default: bool = True
    openai_api_key: Optional[str] = None
    openai_api_base: Optional[str] = None
    google_api_key: Optional[str] = None
    tools: Optional[list] = None

    def __post_init__(self):
        # Set default db_path if not provided
        if self.db_path is None:
            self.db_path = DEFAULT_DB_PATH
        
        # Load API keys from environment if not provided
        if not self.openai_api_key:
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.google_api_key:
            self.google_api_key = os.getenv("GOOGLE_API_KEY")
        if not self.openai_api_base:
            self.openai_api_base = os.getenv("OPENAI_API_BASE")



