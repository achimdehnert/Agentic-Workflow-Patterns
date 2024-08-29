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


    def revise_draft(self, history: str, version: int) -> str:
        """
        Revise the draft based on the history.
        
        Args:
            history (str): The history in Markdown format.
            version (int): The version number of the draft.
        
        Returns:
            str: The revised draft.
        """
        try:
            revised_draft = revise_draft(history=history)
            self.save_to_file(revised_draft, "draft", version)
            return revised_draft
        except Exception as e:
            logger.error(f"Failed to revise draft: {e}")
            raise