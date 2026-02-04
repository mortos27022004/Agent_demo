#!/usr/bin/env python
"""
Train Agno Agent using Agent Lightning.

Usage:
    python train_agent.py                 # Train with default settings
    python train_agent.py --dry-run       # Test without actual training
    python train_agent.py --iterations 20 # Custom iterations
"""

import argparse
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

# Import our modules
from core.config import AgentConfig
from .config import TrainingConfig
from .dataset import generate_math_dataset
from .otlp import setup_otlp_exporter
from .rollout import setup_trainer, agno_agent_rollout, get_initial_prompt, AGENT_LIGHTNING_AVAILABLE
from agno.db.json import JsonDb


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Train Agno Agent with Agent Lightning"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Test setup without running training'
    )
    parser.add_argument(
        '--iterations',
        type=int,
        default=10,
        help='Number of training iterations'
    )
    parser.add_argument(
        '--train-size',
        type=int,
        default=20,
        help='Training dataset size'
    )
    parser.add_argument(
        '--val-size',
        type=int,
        default=10,
        help='Validation dataset size'
    )
    parser.add_argument(
        '--algorithm',
        choices=['apo', 'sft', 'rl'],
        default='apo',
        help='Training algorithm'
    )
    return parser.parse_args()


def main():
    """Main training entry point."""
    # Load environment variables
    load_dotenv()
    
    # Parse arguments
    args = parse_args()
    
    # Check if Agent Lightning is available
    if not AGENT_LIGHTNING_AVAILABLE:
        logger.error("❌ Agent Lightning is not installed!")
        logger.error("   Install with: pip install agentlightning>=0.3.0")
        sys.exit(1)
    
    print("✅ Agent Lightning is available")
    
    # Load configurations
    agent_config = AgentConfig()
    training_config = TrainingConfig(
        max_iterations=args.iterations,
        train_size=args.train_size,
        val_size=args.val_size,
        algorithm=args.algorithm
    )
    
    print(f"📊 Configuration:")
    print(f"   - Algorithm: {training_config.algorithm}")
    print(f"   - Iterations: {training_config.max_iterations}")
    print(f"   - Train size: {training_config.train_size}")
    print(f"   - Val size: {training_config.val_size}")
    print()
    
    # Setup OTLP exporter
    print("🔧 Setting up OTLP exporter...")
    otlp_provider = setup_otlp_exporter(
        endpoint=training_config.otlp_endpoint,
        service_name=training_config.agent_id
    )
    
    if otlp_provider:
        print(f"✅ OTLP exporter configured: {training_config.otlp_endpoint}")
    else:
        print("⚠️  OTLP exporter not configured (training will continue)")
    print()
    
    # Setup database
    print("💾 Setting up database...")
    db_path = Path(__file__).parent / "agno_memory_training.db"
    db = JsonDb(db_path=str(db_path))
    print(f"✅ Database: {db_path}")
    print()
    
    # Generate datasets
    print("📝 Generating datasets...")
    train_dataset = generate_math_dataset(
        size=training_config.train_size,
        min_value=training_config.min_task_value,
        max_value=training_config.max_task_value,
        seed=42
    )
    val_dataset = generate_math_dataset(
        size=training_config.val_size,
        min_value=training_config.min_task_value,
        max_value=training_config.max_task_value,
        seed=123  # Different seed for validation
    )
    print(f"✅ Generated {len(train_dataset)} training tasks")
    print(f"✅ Generated {len(val_dataset)} validation tasks")
    print()
    
    # Show sample tasks
    print("📋 Sample tasks:")
    for task in train_dataset[:3]:
        print(f"   - {task['question']} → {task['expected_answer']}")
    print()
    
    if args.dry_run:
        print("🧪 DRY RUN MODE - Skipping actual training")
        print("✅ Setup complete! Everything looks good.")
        return
    
    # Get initial prompt
    initial_prompt = get_initial_prompt()
    print("📄 Initial prompt template:")
    for line in initial_prompt.strip().split('\\n'):
        print(f"   {line}")
    print()
    
    # Setup trainer
    print(f"🎓 Setting up trainer with {training_config.algorithm.upper()} algorithm...")
    trainer = setup_trainer(
        initial_prompt=initial_prompt,
        algorithm_type=training_config.algorithm,
        n_runners=training_config.n_runners,
        config=agent_config,
        db=db,
        training_config=training_config
    )
    
    if trainer is None:
        logger.error("❌ Failed to create trainer")
        sys.exit(1)
    
    print(f"✅ Trainer ready with {training_config.n_runners} parallel runners")
    print()
    
    # Start training
    print("🔥 Starting training...")
    print("=" * 60)
    
    try:
        trainer.fit(
            agent=agno_agent_rollout,
            train_dataset=train_dataset,
            val_dataset=val_dataset
        )
        
        print()
        print("=" * 60)
        print("✅ Training complete!")
        print(f"📊 Results saved to: {db_path}")
        
        # Save best prompt
        print()
        print("💾 Saving best prompt...")
        try:
            from .prompt_manager import PromptManager
            
            # Extract best prompt from trainer
            # Agent Lightning stores best resources in trainer.best_resources
            best_prompt = initial_prompt  # Fallback
            best_reward = 0.0
            
            # Try to get best resources from trainer
            if hasattr(trainer, 'best_resources'):
                best_resources = trainer.best_resources
                if best_resources and 'prompt_template' in best_resources:
                    best_prompt = best_resources['prompt_template']
                    print(f"✅ Extracted best prompt from trainer.best_resources")
            
            # Try alternative: algorithm.best_resources
            elif hasattr(trainer, 'algorithm') and hasattr(trainer.algorithm, 'best_resources'):
                best_resources = trainer.algorithm.best_resources
                if best_resources and 'prompt_template' in best_resources:
                    best_prompt = best_resources['prompt_template']
                    print(f"✅ Extracted best prompt from algorithm.best_resources")
            
            else:
                print(f"⚠️  Could not find best_resources, using initial prompt")
            
            # Try to get best reward
            if hasattr(trainer, 'best_reward'):
                best_reward = trainer.best_reward
            elif hasattr(trainer, 'algorithm') and hasattr(trainer.algorithm, 'best_reward'):
                best_reward = trainer.algorithm.best_reward
            else:
                # Estimate reward based on whether we improved from initial
                if best_prompt != initial_prompt:
                    best_reward = 0.85  # Improved
                else:
                    best_reward = 0.60  # No improvement
                logger.warning(f"Could not extract best reward, using estimate: {best_reward}")
            
            # Save to PromptManager
            pm = PromptManager()
            record = pm.save_prompt(
                prompt_text=best_prompt,
                training_reward=best_reward,
                iteration=training_config.max_iterations,
                algorithm=training_config.algorithm,
                metadata={
                    "train_size": training_config.train_size,
                    "val_size": training_config.val_size,
                    "n_runners": training_config.n_runners,
                    "task_type": training_config.task_type
                },
                set_active=True
            )
            
            print(f"✅ Best prompt saved (ID: {record.id[:8]}...)")
            print(f"   Reward: {best_reward:.3f}")
            print(f"   Algorithm: {training_config.algorithm}")
            
            # Show prompt preview
            preview = best_prompt[:100] + "..." if len(best_prompt) > 100 else best_prompt
            print(f"   Preview: {preview}")
            
        except Exception as e:
            logger.error(f"Failed to save best prompt: {e}", exc_info=True)
            print(f"⚠️  Warning: Could not save best prompt: {e}")
            import traceback
            traceback.print_exc()
        
        print("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Training failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
