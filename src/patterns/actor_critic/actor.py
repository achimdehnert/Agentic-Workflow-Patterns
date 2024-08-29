from src.config.logging import logger
import json  
import os 


class Actor:
    """
    Handles the creation, review, and revision of drafts, including saving them to files.
    """

    def __init__(self, topic: str):
        self.topic = topic
        self.base_path = "./data/patterns/actor_critic/output"

    def generate_initial_draft(self) -> str:
        """
        Generate the initial draft for the given topic.
        
        Returns:
            str: The generated draft.
        """
        try:
            draft = generate_draft(topic=self.topic)
            self.save_to_file(draft, "draft", 0)
            return draft
        except Exception as e:
            logger.error(f"Failed to generate initial draft: {e}")
            raise