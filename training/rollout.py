"""
Training module cho Agent Lightning integration.

Module này chứa:
- Rollout function với @rollout decorator
- Trainer setup
- Agent creation với custom prompts
"""

import logging
from typing import Optional

try:
    import agentlightning as agl
    from agentlightning.algorithm import APO
    from agentlightning.trainer import Trainer
    from agentlightning.adapter import TraceToMessages
    AGENT_LIGHTNING_AVAILABLE = True
except ImportError:
    AGENT_LIGHTNING_AVAILABLE = False
    agl = None
    APO = None
    Trainer = None
    TraceToMessages = None

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.function import Function
from agno.db.json import JsonDb

from core.config import AgentConfig
from core.tools import sum_1_to_n, calculator
from .dataset import MathTask
from .grader import calculate_reward, extract_answer
from .config import TrainingConfig


logger = logging.getLogger(__name__)


def create_agent_with_prompt(
    prompt_template: str,
    config: AgentConfig,
    db: JsonDb
) -> Agent:
    """
    Create Agno agent with custom prompt template.
    
    Args:
        prompt_template: Prompt template string
        config: Agent configuration
        db: Database instance
        
    Returns:
        Configured Agent instance
    """
    # Split prompt template into instructions
    instructions = [
        line.strip() 
        for line in prompt_template.strip().split('\\n') 
        if line.strip()
    ]
    
    agent = Agent(
        model=OpenAIChat(
            id=config.model_id,
            api_key=config.openai_api_key
        ),
        tools=[
            Function.from_callable(sum_1_to_n),
            Function.from_callable(calculator)
        ],
        instructions=instructions,
        db=db,
        user_id=config.user_id,
        session_id=config.session_id,
        add_history_to_context=False,  # Don't use history during training
        markdown=True,
        debug_mode=False,  # Disable debug during training for cleaner logs
    )
    
    return agent


if AGENT_LIGHTNING_AVAILABLE:
    @agl.rollout
    def agno_agent_rollout(
        task: MathTask,
        prompt_template: agl.PromptTemplate,
        config: AgentConfig = None,
        db: JsonDb = None,
        training_config: TrainingConfig = None
    ) -> float:
        """
        Rollout function for Agent Lightning.
        
        This function is decorated with @agl.rollout to enable
        Agent Lightning training.
        
        Args:
            task: Math task to solve
            prompt_template: Prompt template from Agent Lightning
            config: Agent configuration
            db: Database instance
            training_config: Training configuration
            
        Returns:
            Reward value (0.0 to 1.0)
        """
        # Use defaults if not provided
        if config is None:
            config = AgentConfig()
        if training_config is None:
            training_config = TrainingConfig()
        
        # Create agent with the provided prompt template
        agent = create_agent_with_prompt(
            prompt_template=str(prompt_template),
            config=config,
            db=db
        )
        
        # Run agent on the task
        try:
            response = agent.run(task["question"])
            
            # Calculate reward
            reward = calculate_reward(
                agent_response=response.content,
                expected_answer=task["expected_answer"],
                tolerance=training_config.reward_tolerance,
                use_llm_grader=training_config.use_llm_grader
            )
            
            logger.info(
                f"Task {task['task_id']}: "
                f"Expected={task['expected_answer']}, "
                f"Got={extract_answer(response.content)}, "
                f"Reward={reward:.2f}"
            )
            
            return reward
            
        except Exception as e:
            logger.error(f"Error in rollout for task {task['task_id']}: {e}")
            return 0.0
else:
    # Fallback if Agent Lightning not available
    def agno_agent_rollout(*args, **kwargs) -> float:
        """Fallback rollout function."""
        logger.error("Agent Lightning not installed. Cannot run rollout.")
        return 0.0


def setup_trainer(
    initial_prompt: str,
    algorithm_type: str = "apo",
    n_runners: int = 8,
    config: Optional[AgentConfig] = None,
    db: Optional[JsonDb] = None,
    training_config: Optional[TrainingConfig] = None
) -> Optional[object]:
    """
    Setup Agent Lightning trainer.
    
    Args:
        initial_prompt: Initial prompt template
        algorithm_type: Algorithm type (apo, sft, rl)
        n_runners: Number of parallel runners
        
    Returns:
        Trainer instance or None if Agent Lightning unavailable
    """
    if not AGENT_LIGHTNING_AVAILABLE:
        logger.error("Agent Lightning not installed")
        return None
    
    # Create AsyncOpenAI client for APO algorithm
    from openai import AsyncOpenAI
    import os
    
    async_client = AsyncOpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Choose algorithm
    if algorithm_type == "apo":
        algo = APO(async_openai_client=async_client)
    elif algorithm_type == "sft":
        # SFT not yet supported, fallback to APO
        logger.warning(f"SFT not yet implemented, using APO")
        algo = APO(async_openai_client=async_client)
    elif algorithm_type == "rl":
        # RL not yet supported, fallback to APO
        logger.warning(f"RL not yet implemented, using APO")
        algo = APO(async_openai_client=async_client)
    else:
        logger.warning(f"Unknown algorithm: {algorithm_type}, using APO")
        algo = APO(async_openai_client=async_client)
    
    # Resources to be injected into rollout
    resources = {"prompt_template": initial_prompt}
    if config:
        resources["config"] = config
    if db:
        resources["db"] = db
    if training_config:
        resources["training_config"] = training_config

    # Create trainer
    trainer = Trainer(
        algorithm=algo,
        n_runners=n_runners,
        initial_resources=resources,
        adapter=TraceToMessages(),
    )
    
    logger.info(f"✅ Trainer created with {algorithm_type} algorithm")
    return trainer


def get_initial_prompt() -> str:
    """
    Get default initial prompt template.
    
    Returns:
        Initial prompt string
    """
    return """You are a helpful math assistant.
Solve math problems step by step.
When given a calculation task, use the available tools.
Always show your work and provide the final answer clearly.
Be accurate and precise in your calculations."""
