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
from typing import Optional, Dict, Any


# Default database path for training (relative to project root)
DEFAULT_DB_PATH = str(Path(__file__).parent / "agno_memory.db")



