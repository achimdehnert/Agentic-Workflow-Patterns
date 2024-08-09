from src.patterns.actor_critic.manage.state_manager import StateManager
from src.patterns.actor_critic.orchestrate import Orchestrator
from src.patterns.actor_critic.evaluate import Evaluator
from src.patterns.actor_critic.write import Writer
from src.patterns.actor_critic.route import Router
from src.config.logging import logger


def run() -> None:
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
        logger.error(f"An error occurred in the main orchestration loop: {e}")

if __name__ == "__main__":
    run()
