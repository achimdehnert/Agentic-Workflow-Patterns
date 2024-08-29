from src.patterns.actor_critic.generate import generate_draft
from src.patterns.actor_critic.generate import revise_draft
from src.config.logging import logger
from typing import Any 
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

    def save_to_file(self, content: Any, content_type: str, version: int) -> None:
        """
        Save content to a file under the specified directory and name it with the given version.

        Args:
            content (Any): The content to save. If it is a dict, it will be converted to a string.
            content_type (str): The type of content, either 'draft' or 'feedback'.
            version (int): The version number of the content.
        """
        try:
            directory = os.path.join(self.base_path, content_type)
            os.makedirs(directory, exist_ok=True)
            file_path = os.path.join(directory, f"v{version}.txt")

            if isinstance(content, dict):
                content = json.dumps(content, indent=4)  # Convert dict to a formatted string

            with open(file_path, "w") as file:
                file.write(content)

            logger.info(f"Saved {content_type} v{version} to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save {content_type} v{version}: {e}")
            raise