from src.config.logging import logger
import json  
import os 


class Critic:
    """
    Handles the creation, review, and revision of drafts, including saving them to files.
    """

    def __init__(self, topic: str):
        self.topic = topic
        self.base_path = "./data/patterns/actor_critic/output"

    def review_draft(self, draft: str) -> str:
        """
        Review the provided draft.
        
        Args:
            draft (str): The draft to review.
        
        Returns:
            str: The review of the draft.
        """
        try:
            review = review_draft(draft)
            self.save_to_file(review, "feedback", 0)
            return review
        except Exception as e:
            logger.error(f"Failed to review draft: {e}")
            raise

    def revise_review(self, history: str, version: int) -> str:
        """
        Revise the review based on the history.
        
        Args:
            history (str): The history in Markdown format.
            version (int): The version number of the review.
        
        Returns:
            str: The revised review.
        """
        try:
            revised_review = revise_review(history=history)
            self.save_to_file(revised_review, "feedback", version)
            return revised_review
        except Exception as e:
            logger.error(f"Failed to revise review: {e}")
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