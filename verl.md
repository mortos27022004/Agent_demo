VERL¶
3 months ago
 
3 months ago
 
Yuge Zhang, Zhiyuan He, scott-vsi
Shortcut

You can use the shortcut agl.VERL(...) to create a VERL instance.


import agentlightning as agl

agl.VERL(...)
Installation¶

pip install agentlightning[verl]
Warning

To avoid various compatibility issues, follow the steps in the installation guide to set up VERL and its dependencies. Installing VERL directly with pip install agentlightning[verl] can cause issues unless you already have a compatible version of PyTorch installed.

Notes for Readers

VERL in this article refers to a wrapper, provided by Agent-lightning, of the VERL framework. It's a subclass of agentlightning.Algorithm. To differentiate it from the VERL framework, all references to the VERL framework shall use the term "VERL framework", and all references to the Agent-lightning wrapper shall be highlighted with a link.

Resources¶
VERL expects no initial resources. The first LLM endpoint is directly deployed from the VERL configuration (.actor_rollout_ref.model.path). The resource key is always main_llm.

VERL currently does not support optimizing multiple LLMs together.

Note

The resource type created by VERL is actually a ProxyLLM, a subclass of the LLM type. This object contains a URL template provided by VERL, with placeholders for rollout and attempt IDs. When a rollout begins on the agent side, the framework uses the current rollout_id and attempt_id to format this template, generating a final, unique endpoint URL. This URL points to VERL's internal proxy, allowing it to intercept and log all traffic for that specific attempt, for tracing and load balancing purposes. For agents created with the @rollout decorator, this resolution of the template is handled automatically ("auto-stripped"). Class-based agents will need to manually resolve the ProxyLLM using the rollout context.


proxy_llm = resources["main_llm"]
proxy_llm.get_base_url(rollout.rollout_id, rollout.attempt.attempt_id)
Customization¶
Internally, VERL decomposes each agent execution into prompt–response pairs via the Adapter and associates them with their corresponding reward signals as Triplet objects. The final scalar reward, derived from the last triplet in the trajectory, is propagated to all preceding triplets following the identical assignment strategy. This ensures that each triplet receives an identical reward signal and can be independently optimized as a valid RLHF trajectory within the VERL framework.

At present, VERL does not expose fine-grained control over its reward propagation or credit assignment mechanisms. Users requiring customized reward shaping or trajectory decomposition are advised to clone and modify the VERL source implementation directly.

Tutorials Using VERL¶
Train SQL Agent with RL - A practical example of training a SQL agent using VERL.
References - Entrypoint¶
 agentlightning.algorithm.verl ¶
 VERL ¶
Bases: Algorithm

VERL-powered algorithm that delegates training to the VERL PPO runner.

Warning

Advanced customisation currently requires copying the VERL source and modifying it directly. Native hooks for overriding training behaviour will land in a future release.

Parameters:

config (dict[str, Any]) – Dictionary mirroring the overrides passed to the VERL CLI. The overrides are merged with VERL's packaged defaults via Hydra before launching training.
trainer_cls (Optional[Type[AgentLightningTrainer]], default: None ) – Optional override for the trainer class. Experimental.
daemon_cls (Optional[Type[AgentModeDaemon]], default: None ) – Optional override for the daemon class. Experimental.
Trajectory aggregation (experimental)

Trajectory-level aggregation merges an entire multi-turn rollout into a single, masked training sample so GPU time is spent once per trajectory rather than N times per turn. Enable it via:


config["agentlightning"]["trace_aggregator"] = {
    "level": "trajectory",
    "trajectory_max_prompt_length": 4096,
    "trajectory_max_response_length": 34384,
}
Keep conversations structured (message lists rather than manual string concatenation) so prefix matching can stitch traces. trajectory_max_prompt_length should be set to the maximum length of the prompt for the first turn, and trajectory_max_response_length should be set to the maximum cumulative length of agent responses in the full trajectory. Toggle debug=True plus mismatch_log_dir when you need to inspect retokenization or chat-template mismatches. See this blog post for more details.

Examples:


from agentlightning.algorithm.verl import VERL

algorithm = VERL(
    config={
        "algorithm": {
            "adv_estimator": "grpo",
            "use_kl_in_reward": False,
        },
        "data": {
            "train_batch_size": 32,
            "max_prompt_length": 4096,
            "max_response_length": 2048,
        },
        "actor_rollout_ref": {
            "rollout": {
                "tensor_model_parallel_size": 1,
                "n": 4,
                "log_prob_micro_batch_size_per_gpu": 4,
                "multi_turn": {"format": "hermes"},
                "name": "vllm",
                "gpu_memory_utilization": 0.6,
            },
            "actor": {
                "ppo_mini_batch_size": 32,
                "ppo_micro_batch_size_per_gpu": 4,
                "optim": {"lr": 1e-6},
                "use_kl_loss": False,
                "kl_loss_coef": 0.0,
                "entropy_coeff": 0,
                "clip_ratio_low": 0.2,
                "clip_ratio_high": 0.3,
                "fsdp_config": {
                    "param_offload": True,
                    "optimizer_offload": True,
                },
            },
            "ref": {
                "log_prob_micro_batch_size_per_gpu": 8,
                "fsdp_config": {"param_offload": True},
            },
            "model": {
                "path": "Qwen/Qwen2.5-1.5B-Instruct",
                "use_remove_padding": True,
                "enable_gradient_checkpointing": True,
            },
        },
        "trainer": {
            "n_gpus_per_node": 1,
            "val_before_train": True,
            "critic_warmup": 0,
            "logger": ["console", "wandb"],
            "project_name": "AgentLightning",
            "experiment_name": "calc_x",
            "nnodes": 1,
            "save_freq": 64,
            "test_freq": 32,
            "total_epochs": 2,
        },
    }
)
trainer.fit(algorithm, train_dataset=my_train_dataset)
 get_client() ¶
Create a client bound to the VERL-managed Agent Lightning server.

Deprecated
Since v0.2.

 run(train_dataset=None, val_dataset=None) ¶
Launch the VERL PPO entrypoint with the configured runtime context.

Parameters:

train_dataset (Optional[Dataset[Any]], default: None ) – Optional dataset forwarded to VERL for training.
val_dataset (Optional[Dataset[Any]], default: None ) – Optional dataset forwarded to VERL for evaluation.
Raises:

ValueError – If required dependencies such as the store, LLM proxy, or adapter have been garbage-collected when using the V1 execution mode.
References - Implementation¶
 agentlightning.verl ¶
This package contains a hacky integration of VERL with Agent Lightning.

 AgentLightningTrainer ¶
Bases: RayPPOTrainer

Specialized PPO trainer for agent-based reinforcement learning.

This trainer is designed specifically for scenarios where the model interacts with external environments, tools, or APIs through an AgentLightningServer. It simplifies the training loop by removing the complex conditional logic present in the original RayPPOTrainer and focusing on the agent mode workflow.

Key differences from RayPPOTrainer:

Uses AgentModeDaemon for server communication
Simplified data flow without pop/union operations
Direct batch processing through agent daemon
Streamlined validation using agent_mode validation
 AgentModeDaemon ¶
AgentModeDaemon using the AgentLightningServer SDK.

This class manages the server lifecycle, task queueing, and results retrieval, while also running a proxy server for LLM requests. It maintains the original interface for compatibility with the RayPPOTrainer.

 clear_data_and_server() ¶
Resets the internal state of the daemon for the next run.

 get_test_metrics() ¶
Calculates and returns metrics for a validation run.

 get_train_data_batch(max_prompt_length, max_response_length, device, global_steps) ¶
Processes completed rollouts to generate a training data batch.

This function reconstructs the logic from the original AgentModeDaemon, using data retrieved from the new server architecture. It handles padding, truncation, and tensor creation for the PPO training loop.

 run_until_all_finished(verbose=True) ¶
Synchronously waits for all queued tasks to be completed and reported.

 set_up_data_and_server(data, server_addresses, is_train=True) ¶
Synchronous wrapper for setting up data and server resources.

 start() ¶
Starts the main AgentLightningServer and the proxy server.

 get_left_padded_ids_and_attention_mask(ids, max_length, pad_token_id) ¶
Left-pad (or truncate) a sequence of token IDs to a fixed length, and build the corresponding attention mask.

Parameters:

ids (List[int]) – the original list of token IDs.
max_length (int) – desired total length after padding/truncation.
pad_token_id (int) – ID to use for padding.
Returns:

padded_ids ( any ) – list of length == max_length.
attention_mask ( any ) – list of same length: 1 for non-pad tokens, 0 for pads.
 get_right_padded_ids_and_attention_mask(ids, max_length, pad_token_id) ¶
Right-pad (or truncate) a sequence of token IDs to a fixed length, and build the corresponding attention mask.

Parameters:

ids (List[int]) – the original list of token IDs.
max_length (int) – desired total length after padding/truncation.
pad_token_id (int) – ID to use for padding.
Returns:

padded_ids ( any ) – list of length == max_length.
attention_mask ( any ) – list of same length: 1 for non-pad tokens, 0 for pads.