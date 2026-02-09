import os
import sys
import logging
import argparse
from pathlib import Path
from typing import Tuple, Optional
from dotenv import load_dotenv

from agno.db.json import JsonDb
from core.config import AgentConfig, DEFAULT_DB_PATH
from .config import TrainingConfig
from .data.data_preparation import prepare_datasets
from .engine.rollout import agno_agent_rollout, setup_trainer, get_initial_prompt
from .utils.result_saver import save_training_results
from .utils.store_manager import start_store_server
from .utils.otlp import setup_otlp_exporter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_agent_config() -> AgentConfig:
    """Get Agent configuration from environment variables."""
    db_filename = "agno_memory.db"
    # Prioritize OpenRouter key if available
    api_key = os.getenv("OPENAI_API_KEY_opr") or os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE_URL")

    return AgentConfig(
        model_id="gpt-4o-mini",
        db_filename=db_filename,
        db_path=Path(__file__).parent.parent / "core" / db_filename, # Adjust path as needed
        user_id="user_demo",
        session_id="demo_session",
        num_history_messages=10,
        debug_mode=True,
        use_best_prompt=True,
        fallback_to_default=True,
        openai_api_key=api_key,
        openai_api_base=api_base
    )

def get_training_config(args) -> TrainingConfig:
    """Get Training configuration from arguments."""
    return TrainingConfig(
        n_runners=args.workers,
        max_iterations=args.iterations,
        algorithm=args.algorithm,
        user_data_db_path=args.real_data_db if args.real_data_db else "agno_memory.db",
        otlp_endpoint="http://localhost:4318/v1/traces",
        agent_id="agno-agent-v1"
    )

def main():
    load_dotenv()
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="Train Agno Agent with AgentLightning")
    parser.add_argument("--iterations", type=int, default=1, help="Number of training iterations")
    parser.add_argument("--algorithm", type=str, default="apo", help="Training algorithm (apo, sft, rl)")
    parser.add_argument("--workers", type=int, default=1, help="Number of parallel workers")
    parser.add_argument("--store-url", type=str, default="http://localhost:4747", help="URL for Lightning Store")
    parser.add_argument("--real-data-db", type=str, default=DEFAULT_DB_PATH, help="Path to real user data DB")
    parser.add_argument("--dry-run", action="store_true", help="Run without actual training")
    
    args = parser.parse_args()

    # 1. Setup Infrastructure
    print("\nAttempting to start store server...")
    if not start_store_server(args.store_url):
        print("❌ Store server is required but failed to start. Exiting.")
        return

    # OTLP Setup
    print("🔧 Setting up OTLP exporter...")
    otlp_provider = setup_otlp_exporter(
        endpoint="http://localhost:4318/v1/traces",
        service_name="agno-agent-v1"
    )
    if otlp_provider:
        print(f"✅ OTLP configured: http://localhost:4318/v1/traces")
    else:
        print("⚠️  OTLP not configured")

    # Database Setup
    print("💾 Setting up database...")
    db_path = Path(__file__).parent / "utils" / "agno_memory_training.db"
    db = JsonDb(db_path=str(db_path))
    print(f"✅ Database: {db_path}\n")

    # 2. Configuration
    agent_config = get_agent_config()
    training_config = get_training_config(args)
    
    print(f"📊 Configuration: {training_config.algorithm.upper()}, {training_config.max_iterations} iterations, {training_config.n_runners} workers")

    # 3. Prepare datasets
    train_dataset, val_dataset = prepare_datasets(training_config)
    
    if args.dry_run:
        print("✅ Dry run complete. Exiting.")
        return

    # 4. Create Trainer
    initial_prompt = get_initial_prompt()
    print(f"🎓 Setting up {training_config.algorithm.upper()} trainer...")
    
    trainer = setup_trainer(
        initial_prompt=initial_prompt,
        algorithm_type=training_config.algorithm,
        n_runners=training_config.n_runners,
        config=agent_config,
        db=db,
        training_config=training_config,
        store_url=args.store_url
    )
    
    if not trainer:
        logger.error("❌ Failed to create trainer")
        return
        
    print(f"✅ Trainer ready ({training_config.n_runners} workers)\n")
    
    # 5. Execute Training
    print("🔥 Starting training loop...")
    try:
        trainer.fit(
            agent=agno_agent_rollout,
            train_dataset=train_dataset,
            val_dataset=val_dataset
        )
        print("\n" + "=" * 60)
        print("✅ Training complete!")
        
        # 6. Save results
        save_training_results(trainer, initial_prompt, training_config)
        
    except Exception as e:
        logger.error(f"❌ Training failed: {e}", exc_info=True)
        sys.exit(1)

    print("=" * 60)

if __name__ == "__main__":
    main()
