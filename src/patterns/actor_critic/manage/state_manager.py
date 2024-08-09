from src.config.logging import logger
from datetime import datetime 
from typing import Dict
from typing import Any
import json
import os


STATE_FILE = "state.json"
MAX_CYCLES = 2

class StateManager:
    def __init__(self, state_file: str = STATE_FILE) -> None:
        """
        Initializes the StateManager with the provided state file.

        :param state_file: The path to the JSON file used for storing the state.
        """
        self.state_file = state_file
        self.state = self.load_state()

    def load_state(self) -> Dict[str, Any]:
        """
        Loads the state from the JSON file. If the file doesn't exist, initializes a new state.

        :return: The current state as a dictionary.
        """
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, "r") as file:
                    return json.load(file)
            else:
                return {"cycles": 0, "data": None, "status": "new"}
        except Exception as e:
            logger.error(f"Error loading state: {e}")
            return {"cycles": 0, "data": None, "status": "new"}

    def save_state(self) -> None:
        """
        Saves the current state to the JSON file.
        """
        try:
            with open(self.state_file, "w") as file:
                json.dump(self.state, file, indent=4)
        except Exception as e:
            logger.error(f"Error saving state: {e}")

    def update_state(self, new_data: str, status: str) -> None:
        """
        Updates the state with new data and increments the cycle count.

        :param new_data: The data to be saved in the state.
        :param status: The status of the content (e.g., "approved", "rejected").
        """
        try:
            self.state["cycles"] += 1
            self.state["data"] = new_data
            self.state["status"] = status
            self.state["timestamp"] = datetime.now().isoformat()
            self.save_state()
        except Exception as e:
            logger.error(f"Error updating state: {e}")

    def should_exit(self) -> bool:
        """
        Determines whether the orchestration loop should exit based on the number of cycles.

        :return: True if the maximum number of cycles has been reached, False otherwise.
        """
        return self.state["cycles"] >= MAX_CYCLES
