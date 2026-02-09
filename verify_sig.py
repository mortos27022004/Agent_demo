import sys
from pathlib import Path
import inspect

# Add project root to path
root = Path("/home/lamquy/Project/Agent_demo")
sys.path.insert(0, str(root))

try:
    from core.agent_manager import AgnoAgentManager
    sig = inspect.signature(AgnoAgentManager.initialize)
    print(f"AgnoAgentManager.initialize signature: {sig}")
except Exception as e:
    print(f"Error: {e}")
