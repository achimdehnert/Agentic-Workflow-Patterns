import logging
from src.patterns.actor_critic.state_manager import StateManager

state_manager.state_manager import StateManager
from router.router import Router
from writer.writer import Writer
from evaluator.evaluator import Evaluator
from orchestrator.orchestrator import Orchestrator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main() -> None:
    """
    Main entry point for the application. Initializes all components and runs the orchestration loop.
    """
    try:
        state_manager = StateManager()
        writer = Writer()
        evaluator = Evaluator()
        router = Router(writer, evaluator)
        orchestrator = Orchestrator(state_manager, router)

        while orchestrator.run_cycle():
            pass

    except Exception as e:
        logging.error(f"An error occurred in the main orchestration loop: {e}")

if __name__ == "__main__":
    main()
