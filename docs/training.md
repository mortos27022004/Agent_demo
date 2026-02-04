┌─────────────────────────────────────────────────────────────┐
│  1. INITIALIZATION                                          │
│  ─────────────────                                          │
│  • Load .env (API keys)                                     │
│  • Parse arguments (--iterations, --train-size, --algorithm)│
│  • Check Agent Lightning installed                          │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  2. SETUP CONFIGURATION                                     │
│  ─────────────────────────                                  │
│  • AgentConfig() - API keys, model settings                 │
│  • TrainingConfig() - iterations, dataset sizes, algorithm  │
│  • setup_otlp_exporter() - OTLP tracing                     │
│  • JsonDb() - database for agent memory                     │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  3. GENERATE DATASETS                                       │
│  ────────────────────                                       │
│  • generate_math_dataset(size=20, seed=42) → train_dataset  │
│  • generate_math_dataset(size=10, seed=123) → val_dataset   │
│  • Tasks: "Calculate sum from 1 to N"                       │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  4. SETUP TRAINER                                           │
│  ───────────────                                            │
│  • get_initial_prompt() → prompt template                   │
│  • setup_trainer(prompt, algorithm="apo", n_runners=8)      │
│  • APO algorithm với AsyncOpenAI client                     │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  5. TRAINING LOOP (trainer.fit)                             │
│  ────────────────────────────                               │
│  For each iteration:                                        │
│    ┌───────────────────────────────────────────────────┐    │
│    │  For each task in train_dataset:                  │    │
│    │    • agno_agent_rollout(task, prompt_template)    │    │
│    │    • Agent runs with current prompt               │    │
│    │    • calculate_reward(response, expected_answer)  │    │
│    │    • Return reward (0.0 - 1.0)                    │    │
│    └───────────────────────────────────────────────────┘    │
│    • Aggregate rewards from all tasks                       │
│    • APO optimizes prompt based on rewards                  │
│    • Validate on val_dataset                                │
│    • Keep best prompt if validation improves                │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  6. SAVE BEST PROMPT                                        │
│  ──────────────────                                         │
│  • Extract best prompt from trainer                         │
│  • PromptManager.save_prompt(prompt, reward, metadata)      │
│  • Save to training/best_prompts.json                       │
│  • Set as active prompt                                     │
└─────────────────────────────────────────────────────────────┘