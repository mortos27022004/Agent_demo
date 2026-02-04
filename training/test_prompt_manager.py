"""
Quick test script for PromptManager functionality.

Run this to verify the prompt management system works correctly.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from training.prompt_manager import PromptManager


def test_prompt_manager():
    """Test PromptManager basic functionality."""
    print("=" * 60)
    print("🧪 Testing PromptManager")
    print("=" * 60)
    print()
    
    # Create manager
    test_storage = Path(__file__).parent / "test_prompts.json"
    pm = PromptManager(storage_path=test_storage)
    print(f"✅ Created PromptManager with storage: {test_storage}")
    print()
    
    # Save some test prompts
    print("💾 Saving test prompts...")
    
    prompt1 = pm.save_prompt(
        prompt_text="You are a helpful assistant. Be concise.",
        training_reward=0.75,
        iteration=5,
        algorithm="apo",
        metadata={"test": True, "version": 1}
    )
    print(f"   Saved prompt 1: {prompt1.id[:8]}... (Reward: {prompt1.training_reward})")
    
    prompt2 = pm.save_prompt(
        prompt_text="You are an expert math tutor. Use tools when calculating.",
        training_reward=0.92,
        iteration=10,
        algorithm="apo",
        metadata={"test": True, "version": 2},
        set_active=True
    )
    print(f"   Saved prompt 2: {prompt2.id[:8]}... (Reward: {prompt2.training_reward})")
    print()
    
    # Load best prompt
    print("📖 Loading best prompt...")
    best = pm.load_best_prompt()
    if best:
        print(f"   Best prompt: {best.id[:8]}...")
        print(f"   Reward: {best.training_reward}")
        print(f"   Text: {best.prompt_text[:50]}...")
    print()
    
    # Get history
    print("📚 Getting prompt history...")
    history = pm.get_prompt_history()
    for i, prompt in enumerate(history, 1):
        print(f"   #{i}: Reward={prompt.training_reward:.2f}, Algo={prompt.algorithm}")
    print()
    
    # Get stats
    print("📊 Getting statistics...")
    stats = pm.get_stats()
    print(f"   Total prompts: {stats['total_prompts']}")
    print(f"   Best reward: {stats['best_reward']:.3f}")
    print(f"   Avg reward: {stats['avg_reward']:.3f}")
    print(f"   Algorithms: {', '.join(stats['algorithms_used'])}")
    print()
    
    # Cleanup
    if test_storage.exists():
        test_storage.unlink()
        print("🗑️  Cleaned up test file")
    
    print()
    print("=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    test_prompt_manager()
