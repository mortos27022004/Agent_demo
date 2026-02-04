"""
Demo Agno Agent với OpenAI.

Entry point chính của ứng dụng.
Module này import các components từ:
- core.config: Cấu hình
- core.agent_manager: Quản lý agent
"""

import logging
from dotenv import load_dotenv

from core.config import AgentConfig
from core.agent_manager import AgnoAgentManager


# ========================================
# Logging Configuration
# ========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ========================================
# Main Entry Point
# ========================================
def main() -> None:
    """Entry point chính của ứng dụng."""
    # Load environment variables
    load_dotenv()
    
    # Tạo cấu hình
    config = AgentConfig()
    
    # Khởi tạo agent manager
    manager = AgnoAgentManager(config)
    
    try:
        # Khởi tạo agent
        manager.initialize()
        
        # Danh sách câu hỏi demo
        questions = [
            "Xin chào bạn có thể làm được gì",
        ]
        
        # Chạy câu hỏi
        manager.run_questions(questions)
        
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        print(f"\n❌ Lỗi: {e}")
        return


if __name__ == "__main__":
    main()

