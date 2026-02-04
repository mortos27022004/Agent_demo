"""
Prompt Manager for Agent Lightning Training.

Simplified version for saving and loading best prompts.
"""

import json
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


@dataclass
class PromptRecord:
    """Record of a trained prompt with metadata."""
    id: str
    prompt_text: str
    timestamp: str
    training_reward: float
    iteration: int
    algorithm: str
    is_active: bool = False
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create PromptRecord from dictionary."""
        return cls(**data)
    
    def to_dict(self):
        """Convert to dictionary."""
        return asdict(self)


class PromptManager:
    """Manager for best prompt persistence."""
    
    def __init__(self, storage_path: Optional[Path] = None):
        """Initialize PromptManager."""
        if storage_path is None:
            storage_path = Path(__file__).parent / "best_prompts.json"
        
        self.storage_path = Path(storage_path)
        
        if not self.storage_path.exists() or self.storage_path.stat().st_size == 0:
            self._init_storage()
    
    def _init_storage(self):
        """Initialize empty storage file."""
        data = {"version": "1.0", "prompts": []}
        self._write_storage(data)
    
    def _read_storage(self) -> dict:
        """Read storage file with fallback for empty files."""
        try:
            if self.storage_path.stat().st_size == 0:
                return {"version": "1.0", "prompts": []}
                
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # If corrupt or missing, return empty structure
            return {"version": "1.0", "prompts": []}
    
    def _write_storage(self, data: dict):
        """Write to storage file."""
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def save_prompt(
        self,
        prompt_text: str,
        training_reward: float,
        iteration: int,
        algorithm: str = "apo",
        metadata: Optional[Dict[str, Any]] = None,
        set_active: bool = True
    ) -> PromptRecord:
        """
        Save a new trained prompt.
        
        Args:
            prompt_text: The prompt template text
            training_reward: Final training reward score
            iteration: Number of training iterations
            algorithm: Training algorithm used
            metadata: Additional metadata
            set_active: Whether to set this as active prompt
            
        Returns:
            Saved PromptRecord
        """
        # Read current data
        data = self._read_storage()
        
        # Create new record
        record = PromptRecord(
            id=str(uuid.uuid4()),
            prompt_text=prompt_text,
            timestamp=datetime.now().isoformat(),
            training_reward=training_reward,
            iteration=iteration,
            algorithm=algorithm,
            is_active=set_active,
            metadata=metadata or {}
        )
        
        # Deactivate all others if setting this as active
        if set_active:
            for prompt in data["prompts"]:
                prompt["is_active"] = False
        
        # Add to storage
        data["prompts"].append(record.to_dict())
        self._write_storage(data)
        
        logger.info(
            f"✅ Saved prompt (ID: {record.id[:8]}..., "
            f"Reward: {record.training_reward:.3f}, "
            f"Algorithm: {record.algorithm})"
        )
        
        return record
    
    def load_best_prompt(self) -> Optional[PromptRecord]:
        """Load the best prompt (highest reward)."""
        data = self._read_storage()
        prompts = data.get("prompts", [])
        
        if not prompts:
            return None
        
        # Find best by reward
        best = max(prompts, key=lambda p: p.get("training_reward", 0.0))
        return PromptRecord.from_dict(best)
    
    def load_active_prompt(self) -> Optional[PromptRecord]:
        """Load the currently active prompt."""
        data = self._read_storage()
        prompts = data.get("prompts", [])
        
        # Find active prompt
        for prompt in prompts:
            if prompt.get("is_active", False):
                return PromptRecord.from_dict(prompt)
        
        return None
    
    def get_prompt_history(self, limit: Optional[int] = None) -> List[PromptRecord]:
        """Get prompt history sorted by timestamp."""
        data = self._read_storage()
        prompts = data.get("prompts", [])
        
        # Sort by timestamp (newest first)
        sorted_prompts = sorted(
            prompts,
            key=lambda p: p.get("timestamp", ""),
            reverse=True
        )
        
        if limit:
            sorted_prompts = sorted_prompts[:limit]
        
        return [PromptRecord.from_dict(p) for p in sorted_prompts]
