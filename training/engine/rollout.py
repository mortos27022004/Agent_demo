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
    from agentlightning import LightningStoreClient
    AGENT_LIGHTNING_AVAILABLE = True
except ImportError:
    AGENT_LIGHTNING_AVAILABLE = False
    agl = None
    APO = None
    Trainer = None
    TraceToMessages = None
    LightningStoreClient = None

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.function import Function
from agno.db.json import JsonDb

from core.config import AgentConfig

from .grader import calculate_reward
from ..config import TrainingConfig


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
    
    # Get tools from config if available, otherwise use empty list
    tools = getattr(config, 'tools', [])
    
    agent = Agent(
        model=OpenAIChat(
            id=config.model_id,
            api_key=config.openai_api_key,
            base_url=config.openai_api_base
        ),
        tools=tools,
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
        task: dict,
        prompt_template: agl.PromptTemplate,
        **resources
    ) -> float:
        """
        Rollout function for Agent Lightning.
        
        This function is decorated with @agl.rollout to enable
        Agent Lightning training.
        
        Args:
            task: Training task to solve
            prompt_template: Prompt template from Agent Lightning
            config: Agent configuration
            db: Database instance
            training_config: Training configuration
            
        Returns:
            Reward value (0.0 to 1.0)
        """
        # Extract resources
        config = resources.get("config")
        db = resources.get("db")
        training_config = resources.get("training_config")
        
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
                question=task["question"],
                use_llm_grader=training_config.use_llm_grader
            )
            
            logger.info(
                f"Task {task['task_id']}: "
                f"Q='{task['question'][:50]}...', "
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
    n_runners: int = 1,
    config: Optional[AgentConfig] = None,
    db: Optional[JsonDb] = None,
    training_config: Optional[TrainingConfig] = None,
    store_url: Optional[str] = None
) -> Optional[object]:
    """
    Setup Agent Lightning trainer.
    
    Args:
        initial_prompt: Initial prompt template
        algorithm_type: Algorithm type (apo, sft, rl)
        n_runners: Number of parallel runners
        store_url: External store URL for debugging (e.g., "http://localhost:4747")
        
    Returns:
        Trainer instance or None if Agent Lightning unavailable
    """
    if not AGENT_LIGHTNING_AVAILABLE:
        logger.error("Agent Lightning not installed")
        return None
    
    # Create AsyncOpenAI client for APO algorithm
    from openai import AsyncOpenAI
    import os
    
    # Use config from argument if available, else from env
    api_key = config.openai_api_key if config else os.getenv("OPENAI_API_KEY_opr") or os.getenv("OPENAI_API_KEY")
    base_url = config.openai_api_base if config else os.getenv("OPENAI_API_BASE_URL")

    async_client = AsyncOpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    # Choose algorithm
    if algorithm_type == "apo":
        # APO Configuration with tuned hyperparameters
        # Based on agentlightning documentation best practices
        algo = APO(
            async_openai_client=async_client,
            # Model configuration (override defaults which are invalid)
            gradient_model="gpt-4o-mini",      # For computing textual gradients/critiques
            apply_edit_model="gpt-4o-mini",    # For applying edits based on critiques
            
            # Beam search parameters
            beam_width=2,                       # Top-k prompts to keep per round
            branch_factor=1,                    # New candidates per parent prompt
            beam_rounds=1,                      # Number of optimization rounds
            
            # Sampling parameters
            gradient_batch_size=4,              # Rollouts sampled for gradient computation
            val_batch_size=8,                  # Validation examples per evaluation
            
            # Optimization parameters
            diversity_temperature=1.0,          # Temperature for diversity in generation
            rollout_batch_timeout=3600.0,       # Max wait time for rollout completion (seconds)
            run_initial_validation=True,        # Establish baseline before optimization
        )

    prompt_resource = agl.PromptTemplate(
        template=initial_prompt,
        engine="f-string"
    )

    resources = {
        "main_prompt": prompt_resource,
        "config": config,
        "db": db,
        "training_config": training_config
    }

    store = None
    if store_url:
        try:
            store = LightningStoreClient(store_url)
            logger.info(f"✅ Connected to external store: {store_url}")
        except Exception as e:
            logger.warning(f"⚠️ Could not connect to external store: {e}")
            store = None

    trainer = Trainer(
        algorithm=algo,
        n_runners=n_runners,
        initial_resources=resources,
        adapter=TraceToMessages(),
        store=store,  # Use external store if available
    )
    
    logger.info(f"✅ Trainer created with {algorithm_type} algorithm")
    return trainer


def get_initial_prompt() -> str:

    from core.prompts import INITIAL_TRAINING_PROMPT
    return INITIAL_TRAINING_PROMPT
