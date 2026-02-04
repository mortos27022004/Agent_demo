#!/usr/bin/env python
"""Infrastructure setup module for OTLP and database."""

from pathlib import Path

from agno.db.json import JsonDb
from ..config import TrainingConfig
from .otlp import setup_otlp_exporter


def setup_infrastructure(training_config: TrainingConfig) -> JsonDb:
    """
    Setup OTLP exporter and database.
    
    Args:
        training_config: Training configuration
        
    Returns:
        JsonDb instance
    """
    # OTLP exporter
    print("🔧 Setting up OTLP exporter...")
    otlp_provider = setup_otlp_exporter(
        endpoint=training_config.otlp_endpoint,
        service_name=training_config.agent_id
    )
    status = f"✅ OTLP: {training_config.otlp_endpoint}" if otlp_provider else "⚠️  OTLP not configured"
    print(f"{status}\n")
    
    # Database
    print("💾 Setting up database...")
    db_path = Path(__file__).parent / "agno_memory_training.db"
    db = JsonDb(db_path=str(db_path))
    print(f"✅ Database: {db_path}\n")
    
    return db
