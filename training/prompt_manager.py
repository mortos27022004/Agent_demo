"""
Prompt Manager for Agent Lightning Training.

This module manages saving, loading, and tracking best prompts
from Agent Lightning training sessions.
"""

import json
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime

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
        """Initialize metadata if not provided."""
        if self.metadata is None:
            self.metadata = {}
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PromptRecord':
        """Create PromptRecord from dictionary."""
        return cls(**data)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


class PromptManager:
    """Manager for best prompt persistence."""
    
    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize PromptManager.
        
        Args:
            storage_path: Path to JSON storage file
        """
        if storage_path is None:
            # Default to training/best_prompts.json
            storage_path = Path(__file__).parent / "best_prompts.json"
        
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize storage if not exists
        if not self.storage_path.exists():
            self._init_storage()
    
    def _init_storage(self) -> None:
        """Initialize empty storage file."""
        initial_data = {
            "version": "1.0",
            "prompts": []
        }
        self._write_storage(initial_data)
        logger.info(f"Initialized prompt storage at: {self.storage_path}")
    
    def _read_storage(self) -> dict:
        """Read storage file."""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading prompt storage: {e}")
            return {"version": "1.0", "prompts": []}
    
    def _write_storage(self, data: dict) -> None:
        """Write to storage file."""
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error writing prompt storage: {e}")
            raise
    
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
            set_active: Whether to set this as the active prompt
            
        Returns:
            Created PromptRecord
        """
        import uuid
        
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
        
        # Load current storage
        data = self._read_storage()
        
        # Deactivate all prompts if setting this as active
        if set_active:
            for prompt in data["prompts"]:
                prompt["is_active"] = False
        
        # Add new prompt
        data["prompts"].append(record.to_dict())
        
        # Save
        self._write_storage(data)
        
        logger.info(
            f"✅ Saved prompt (ID: {record.id[:8]}..., "
            f"Reward: {training_reward:.3f}, "
            f"Algorithm: {algorithm})"
        )
        
        return record
    
    def load_best_prompt(self) -> Optional[PromptRecord]:
        """
        Load the best prompt (highest reward).
        
        Returns:
            PromptRecord with highest training_reward, or None if no prompts
        """
        data = self._read_storage()
        prompts = data.get("prompts", [])
        
        if not prompts:
            logger.warning("No prompts found in storage")
            return None
        
        # Convert to PromptRecord objects
        records = [PromptRecord.from_dict(p) for p in prompts]
        
        # Find highest reward
        best = max(records, key=lambda r: r.training_reward)
        
        logger.info(
            f"Loaded best prompt (Reward: {best.training_reward:.3f}, "
            f"Algorithm: {best.algorithm})"
        )
        
        return best
    
    def load_active_prompt(self) -> Optional[PromptRecord]:
        """
        Load the currently active prompt.
        
        Returns:
            Active PromptRecord, or None if no active prompt
        """
        data = self._read_storage()
        prompts = data.get("prompts", [])
        
        for prompt_data in prompts:
            if prompt_data.get("is_active", False):
                return PromptRecord.from_dict(prompt_data)
        
        return None
    
    def get_prompt_history(
        self,
        limit: Optional[int] = None,
        sort_by: str = "timestamp"
    ) -> List[PromptRecord]:
        """
        Get prompt history.
        
        Args:
            limit: Maximum number of prompts to return
            sort_by: Sort field ("timestamp" or "training_reward")
            
        Returns:
            List of PromptRecords sorted by specified field (descending)
        """
        data = self._read_storage()
        prompts = data.get("prompts", [])
        
        if not prompts:
            return []
        
        # Convert to PromptRecord objects
        records = [PromptRecord.from_dict(p) for p in prompts]
        
        # Sort
        if sort_by == "training_reward":
            records.sort(key=lambda r: r.training_reward, reverse=True)
        else:  # timestamp
            records.sort(key=lambda r: r.timestamp, reverse=True)
        
        # Apply limit
        if limit:
            records = records[:limit]
        
        return records
    
    def set_active_prompt(self, prompt_id: str) -> bool:
        """
        Set a specific prompt as active.
        
        Args:
            prompt_id: ID of prompt to activate
            
        Returns:
            True if successful, False otherwise
        """
        data = self._read_storage()
        prompts = data.get("prompts", [])
        
        found = False
        for prompt in prompts:
            if prompt["id"] == prompt_id:
                prompt["is_active"] = True
                found = True
            else:
                prompt["is_active"] = False
        
        if found:
            self._write_storage(data)
            logger.info(f"Activated prompt: {prompt_id[:8]}...")
            return True
        else:
            logger.warning(f"Prompt not found: {prompt_id}")
            return False
    
    def compare_prompts(
        self,
        prompt_id_1: str,
        prompt_id_2: str
    ) -> Dict[str, Any]:
        """
        Compare two prompts by their metrics.
        
        Args:
            prompt_id_1: First prompt ID
            prompt_id_2: Second prompt ID
            
        Returns:
            Comparison dictionary with metrics
        """
        data = self._read_storage()
        prompts = {p["id"]: p for p in data.get("prompts", [])}
        
        if prompt_id_1 not in prompts or prompt_id_2 not in prompts:
            raise ValueError("One or both prompt IDs not found")
        
        p1 = prompts[prompt_id_1]
        p2 = prompts[prompt_id_2]
        
        return {
            "prompt_1": {
                "id": p1["id"],
                "reward": p1["training_reward"],
                "algorithm": p1["algorithm"],
                "timestamp": p1["timestamp"]
            },
            "prompt_2": {
                "id": p2["id"],
                "reward": p2["training_reward"],
                "algorithm": p2["algorithm"],
                "timestamp": p2["timestamp"]
            },
            "reward_improvement": p2["training_reward"] - p1["training_reward"],
            "better": prompt_id_2 if p2["training_reward"] > p1["training_reward"] else prompt_id_1
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about stored prompts.
        
        Returns:
            Statistics dictionary
        """
        data = self._read_storage()
        prompts = data.get("prompts", [])
        
        if not prompts:
            return {
                "total_prompts": 0,
                "best_reward": None,
                "avg_reward": None,
                "algorithms_used": []
            }
        
        rewards = [p["training_reward"] for p in prompts]
        algorithms = list(set(p["algorithm"] for p in prompts))
        
        return {
            "total_prompts": len(prompts),
            "best_reward": max(rewards),
            "avg_reward": sum(rewards) / len(rewards),
            "worst_reward": min(rewards),
            "algorithms_used": algorithms,
            "active_prompt_id": next(
                (p["id"] for p in prompts if p.get("is_active")),
                None
            )
        }
