import os
from dotenv import load_dotenv

from pathlib import Path
from .setup import initialize_training
from .data.data_preparation import prepare_datasets
from .engine.executor import run_training
from .utils.result_saver import save_training_results
from .utils.store_manager import start_store_server
from core.config import DEFAULT_DB_PATH

def main(
    iterations: int = 1,
    algorithm: str = "apo",
    workers: int = 1,
    store_url: str = "http://localhost:4747",
    real_data_db: str = DEFAULT_DB_PATH
):
    load_dotenv()
    # Auto-start store server if needed
    if not start_store_server(store_url):
        print("❌ Store server is required but failed to start. Exiting.")
        return
    
    agent_config = get_agent_config()

    training_config = get_training_config(
        iterations=iterations,
        algorithm=algorithm,
        n_runners=workers,
        real_data_db=real_data_db
    )
    
    db = setup_infrastructure(training_config)
    
    # 2. Prepare datasets
    train_dataset, val_dataset = prepare_datasets(training_config)
    
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
    main()
