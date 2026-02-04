#!/usr/bin/env python
"""Train Agno Agent using Agent Lightning.

This is the main orchestrator that coordinates the training workflow.
"""

import logging
import os
from dotenv import load_dotenv

from pathlib import Path
from .setup import initialize_training
from .data.data_preparation import prepare_datasets
from .engine.training_executor import run_training
from .utils.result_saver import save_training_results

# Create logs directory
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_dir / "training.log", mode='a')
    ]
)
logger = logging.getLogger(__name__)


# Default database path relative to project root
DEFAULT_DB_PATH = str(Path(__file__).parent.parent / "core" / "agno_memory.db")


def main(
    iterations: int = 1,
    algorithm: str = "apo",
    store_url: str = None,
    dry_run: bool = False,
    real_data_db: str = DEFAULT_DB_PATH
):
    """
    Simplified training entry point.
    """
    load_dotenv()
    
    # Troubleshooting support (per user tips)
    if os.getenv("AGENTOPS_LOG_LEVEL") == "DEBUG":
        print("🔍 AgentOps Debug Mode Enabled")
    
    if not os.getenv("AGENTOPS_API_KEY"):
        print("⚠️ Warning: AGENTOPS_API_KEY not found in environment.")
        print("   If you want to trace training sessions, add it to your .env file.")
    # 1. Initialize (Dependencies + Config + Infrastructure)
    agent_config, training_config, db = initialize_training(
        iterations=iterations,
        algorithm=algorithm,
        real_data_db=real_data_db
    )
    
    # 2. Prepare datasets
    train_dataset, val_dataset = prepare_datasets(training_config)
    
    if dry_run:
        print("🧪 DRY RUN MODE - Setup complete!")
        return
    print (train_dataset)
    if store_url:
        # If using external store (dashboard), tell agentlightning NOT to start
        # its own internal server wrapper for subprocesses. This avoids binding
        # conflicts and timeout issues.
        os.environ["AGL_MANAGED_STORE"] = "false"
        print(f"🔗 Using external store: {store_url}")
    
    # 3. Create trainer and Execute training
    trainer, initial_prompt = run_training(
        training_config=training_config,
        agent_config=agent_config,
        db=db,
        train_dataset=train_dataset,
        val_dataset=val_dataset,
        store_url=store_url
    )
    
    # 4. Save results
    save_training_results(trainer, initial_prompt, training_config)
    
    print("=" * 60)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Agno Agent Training Pipeline")
    parser.add_argument("--iterations", type=int, default=1, help="Number of training iterations")
    parser.add_argument("--algorithm", type=str, default="apo", help="Training algorithm (apo, sft, rl)")
    parser.add_argument("--store-url", type=str, help="Optional external store URL")
    parser.add_argument("--dry-run", action="store_true", help="Only setup and prepare data without training")
    parser.add_argument("--real-data-db", type=str, default=DEFAULT_DB_PATH, help="Path to real data database")
    
    args = parser.parse_args()
    
    main(
        iterations=args.iterations,
        algorithm=args.algorithm,
        store_url=args.store_url,
        dry_run=args.dry_run,
        real_data_db=args.real_data_db
    )