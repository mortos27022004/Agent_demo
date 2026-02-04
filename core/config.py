"""
Configuration module cho Agno Agent.

Module này chứa tất cả cấu hình cho agent, bao gồm:
- Model settings
- Database paths
- User và session IDs
- Debug mode
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class AgentConfig:
    """Cấu hình cho Agno Agent."""
    
    model_id: str = "gpt-4o-mini"
    db_filename: str = "agno_memory.db"
    user_id: str = "user_demo"
    session_id: str = "demo_session"
    num_history_messages: int = 10
    debug_mode: bool = True
    
    # Prompt management
    use_best_prompt: bool = True  # Auto-use trained prompt
    fallback_to_default: bool = True  # Fallback if no best prompt exists
    
    @property
    def db_path(self) -> Path:
        """Đường dẫn đầy đủ tới database file."""
        return Path(__file__).parent / self.db_filename
    
    @property
    def openai_api_key(self) -> Optional[str]:
        """Lấy OpenAI API key từ environment variables."""
        return os.getenv("OPENAI_API_KEY")
