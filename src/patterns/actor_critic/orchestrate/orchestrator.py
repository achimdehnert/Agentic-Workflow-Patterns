import logging
from state_manager.state_manager import StateManager
from router.router import Router

class Orchestrator:
    def __init__(self, state_manager: StateManager, router: Router) -> None:
        """
        Initializes the Orchestrator with a state manager and a router.

        :param state_manager: An instance of StateManager to handle state persistence.
        :param router: An instance of Router to handle the flow of data between components.
        """
        self.state_manager = state_manager
        self.router = router

    def run_cycle(self) -> bool:
        """
        Runs a single cycle of the orchestration process, passing data through the writer and evaluator.
        It updates the state and decides whether to continue or exit the loop.

        :return: False if the loop should exit, True otherwise.
        """
        try:
            current_data = self.state_manager.state["data"] or "Write a blog post about AI advancements"
            logging.info(f"Cycle {self.state_manager.state['cycles'] + 1}: Input data: {current_data}")
            
            # Route data through Writer and Evaluator
            processed_data, status = self.router.route(current_data, self.state_manager.state['cycles'])
            logging.info(f"Cycle {self.state_manager.state['cycles'] + 1}: Processed data: {processed_data}, Status: {status}")
            
            # Update state
            self.state_manager.update_state(processed_data, status)

            if self.state_manager.should_exit() or status == "approved":
                logging.info("Exiting due to either maximum cycles reached or content approved.")
                return False
            return True

        except Exception as e:
            logging.error(f"An error occurred during the orchestration cycle: {e}")
            return False
