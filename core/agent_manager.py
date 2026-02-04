"""
Agent Manager module cho Agno Agent.

Module này chứa class AgnoAgentManager để quản lý:
- Khởi tạo database
- Setup tracing
- Tạo và cấu hình agent
- Chạy câu hỏi qua agent
"""

import logging
from typing import List, Optional

from agno.agent import Agent
from agno.db.json import JsonDb
from agno.models.openai import OpenAIChat
from agno.tools.function import Function
from agno.tracing import setup_tracing

from .config import AgentConfig
from .tools import sum_1_to_n, calculator


logger = logging.getLogger(__name__)


class AgnoAgentManager:
    """Quản lý việc khởi tạo và chạy Agno Agent."""
    
    def __init__(self, config: AgentConfig):
        """
        Khởi tạo Agent Manager.
        
        Args:
            config: Cấu hình agent
        """
        self.config = config
        self.db: Optional[JsonDb] = None
        self.agent: Optional[Agent] = None
        
    def setup_database(self) -> JsonDb:
        """
        Thiết lập JSON database.
        
        Returns:
            JsonDb instance
        """
        logger.info(f"Initializing database at: {self.config.db_path}")
        self.db = JsonDb(db_path=str(self.config.db_path))
        return self.db
    
    def setup_tracing(self) -> None:
        """
        Thiết lập OpenTelemetry tracing.
        
        Raises:
            RuntimeError: Nếu database chưa được khởi tạo
        """
        if self.db is None:
            raise RuntimeError("Database must be initialized before setting up tracing")
        
        setup_tracing(db=self.db)
        logger.info("OpenTelemetry tracing enabled")
    
    def create_agent(self) -> Agent:
        """
        Tạo Agno Agent với cấu hình đã thiết lập.
        
        Returns:
            Agent instance
            
        Raises:
            ValueError: Nếu API key không được cung cấp
            RuntimeError: Nếu database chưa được khởi tạo
        """
        if not self.config.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        if self.db is None:
            raise RuntimeError("Database must be initialized before creating agent")
        
        logger.info(f"Creating agent with model: {self.config.model_id}")
        
        # Get instructions (from best prompt or default)
        instructions = self._get_instructions()
        
        self.agent = Agent(
            model=OpenAIChat(
                id=self.config.model_id,
                api_key=self.config.openai_api_key
            ),
            tools=[
                Function.from_callable(sum_1_to_n),
                Function.from_callable(calculator)
            ],
            instructions=instructions,
            db=self.db,
            user_id=self.config.user_id,
            session_id=self.config.session_id,
            add_history_to_context=False,
            num_history_messages=self.config.num_history_messages,
            markdown=True,
            debug_mode=self.config.debug_mode,
        )
        
        return self.agent
    
    def _get_instructions(self) -> List[str]:
        """
        Get instructions from best prompt or default.
        
        Returns:
            List of instruction strings
        """
        # Try to load best prompt if enabled
        if self.config.use_best_prompt:
            try:
                # Import here to avoid circular dependency
                import sys
                from pathlib import Path
                sys.path.insert(0, str(Path(__file__).parent.parent))
                
                from training.prompt_manager import PromptManager
                
                pm = PromptManager()
                best_prompt = pm.load_best_prompt()
                
                if best_prompt:
                    logger.info(
                        f"✅ Using best prompt from training "
                        f"(Reward: {best_prompt.training_reward:.3f}, "
                        f"Algorithm: {best_prompt.algorithm})"
                    )
                    # Split prompt into instructions lines
                    instructions = [
                        line.strip() 
                        for line in best_prompt.prompt_text.strip().split('\n') 
                        if line.strip()
                    ]
                    return instructions
                else:
                    logger.info("No best prompt found, using default instructions")
                    
            except Exception as e:
                logger.warning(f"Failed to load best prompt: {e}")
                if self.config.fallback_to_default:
                    logger.info("Falling back to default instructions")
                else:
                    raise
        
        # Default instructions
        logger.info("Using default instructions")
        return [
            "Bạn là một trợ lý AI thông minh và hữu ích.",
            "Khi cần tính toán, hãy SỬ DỤNG TOOL thay vì tự tính.",
            "Luôn giải thích rõ ràng cách bạn sử dụng tool.",
            "Trả lời bằng tiếng Việt trừ khi được yêu cầu khác."
        ]
    
    def initialize(self) -> None:
        """
        Khởi tạo đầy đủ: database, tracing, và agent.
        
        Phương thức này sẽ:
        1. Setup database
        2. Enable tracing
        3. Tạo agent
        """
        self.setup_database()
        self.setup_tracing()
        self.create_agent()
        logger.info("Agent initialization complete")
    
    def create_agent_with_prompt(self, prompt_template: str) -> Agent:
        """
        Tạo agent với custom prompt template.
        
        Được sử dụng trong Agent Lightning training để test
        các prompt templates khác nhau.
        
        Args:
            prompt_template: Prompt template string
            
        Returns:
            Agent instance với prompt mới
        """
        if not self.config.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        if self.db is None:
            raise RuntimeError("Database must be initialized before creating agent")
        
        # Parse prompt template into instructions
        instructions = [
            line.strip() 
            for line in prompt_template.strip().split('\n') 
            if line.strip()
        ]
        
        logger.info(f"Creating agent with custom prompt ({len(instructions)} instructions)")
        
        self.agent = Agent(
            model=OpenAIChat(
                id=self.config.model_id,
                api_key=self.config.openai_api_key
            ),
            tools=[
                Function.from_callable(sum_1_to_n),
                Function.from_callable(calculator)
            ],
            instructions=instructions,
            db=self.db,
            user_id=self.config.user_id,
            session_id=self.config.session_id,
            add_history_to_context=False,  # Disable history for training
            num_history_messages=0,
            markdown=True,
            debug_mode=False,
        )
        
        return self.agent
    
    def run_questions(self, questions: List[str]) -> None:
        """
        Chạy danh sách câu hỏi qua agent.
        
        Args:
            questions: Danh sách các câu hỏi
            
        Raises:
            RuntimeError: Nếu agent chưa được khởi tạo
        """
        if self.agent is None:
            raise RuntimeError("Agent must be initialized before running questions")
        
        print("=" * 60)
        print(f"📁 Database: {self.config.db_path.absolute()}")
        print("=" * 60)
        print()
        
        for i, question in enumerate(questions, 1):
            print(f"\n{'─' * 60}")
            print(f"❓ Câu hỏi {i}: {question}")
            print(f"{'─' * 60}\n")
            
            try:
                response = self.agent.run(question)
                print(f"🤖 Agent trả lời:\n{response.content}\n")
            except Exception as e:
                logger.error(f"Error processing question {i}: {e}", exc_info=True)
                print(f"❌ Lỗi khi xử lý câu hỏi: {e}\n")
        
        print("=" * 60)
        print("✅ Demo hoàn tất!")
        print(f"📝 Lịch sử hội thoại đã được lưu vào: {self.config.db_path.absolute()}")
        print("=" * 60)
