from src.patterns.actor_critic.generate.generator import generate_draft
from src.patterns.actor_critic.generate.generator import revise_review
from src.patterns.actor_critic.generate.generator import review_draft
from src.patterns.actor_critic.generate.generator import revise_draft
from src.config.logging import logger
from collections import OrderedDict
from typing import Dict
from typing import Any 


class HistoryManager:
    """
    Manages the history of drafts and reviews, and provides functionality to convert it into Markdown format.
    """
    
    def __init__(self):
        self.history = OrderedDict()
        self.history_md = None

    def add_entry(self, key: str, value: Any) -> None:
        """
        Add an entry to the history.
        
        Args:
            key (str): The key for the history entry.
            value (Any): The value for the history entry.
        """
        self.history[key] = value
        self.history_md = self.to_markdown()

    def to_markdown(self) -> str:
        """
        Convert the history to a Markdown formatted string.
        
        Returns:
            str: A Markdown formatted string representing the history.
        """
        markdown = []

        for key, value in self.history.items():
            markdown.append(f"### {key}\n")
            if isinstance(value, dict):
                markdown.append(f"```\n{self.dict_to_markdown(value)}\n```")
            else:
                markdown.append(f"```\n{value}\n```")
            markdown.append("\n")  

        return ''.join(markdown)

    @staticmethod
    def dict_to_markdown(data: Dict[str, Any], indent_level: int = 0) -> str:
        """
        Convert a dictionary to a Markdown formatted string with a given indentation level.
        
        Args:
            data (dict): The dictionary to convert.
            indent_level (int): The current level of indentation for nested dictionaries.
        
        Returns:
            str: A Markdown formatted string representing the dictionary.
        """
        markdown = []
        indent = ' ' * indent_level

        for key, value in data.items():
            if isinstance(value, dict):
                markdown.append(f"{indent}- **{key.capitalize()}**:\n")
                markdown.append(HistoryManager.dict_to_markdown(value, indent_level + 2))  # Recursive call for nested dicts
            else:
                markdown.append(f"{indent}- **{key.capitalize()}**: {value}\n")

        return ''.join(markdown)

    def get_history(self) -> OrderedDict:
        """
        Get the current history.
        
        Returns:
            OrderedDict: The history containing drafts and reviews.
        """
        return self.history


class DraftManager:
    """
    Handles the creation, review, and revision of drafts.
    """

    def __init__(self, topic: str):
        self.topic = topic

    def generate_initial_draft(self) -> str:
        """
        Generate the initial draft for the given topic.
        
        Returns:
            str: The generated draft.
        """
        try:
            return generate_draft(topic=self.topic)
        except Exception as e:
            logger.error(f"Failed to generate initial draft: {e}")
            raise

    def review_draft(self, draft: str) -> str:
        """
        Review the provided draft.
        
        Args:
            draft (str): The draft to review.
        
        Returns:
            str: The review of the draft.
        """
        try:
            return review_draft(draft)
        except Exception as e:
            logger.error(f"Failed to review draft: {e}")
            raise

    def revise_draft(self, history: str) -> str:
        """
        Revise the draft based on the history.
        
        Args:
            history (str): The history in Markdown format.
        
        Returns:
            str: The revised draft.
        """
        try:
            return revise_draft(history=history)
        except Exception as e:
            logger.error(f"Failed to revise draft: {e}")
            raise

    def revise_review(self, history: str) -> str:
        """
        Revise the review based on the history.
        
        Args:
            history (str): The history in Markdown format.
        
        Returns:
            str: The revised review.
        """
        try:
            return revise_review(history=history)
        except Exception as e:
            logger.error(f"Failed to revise review: {e}")
            raise


class ActorCriticPipeline:
    """
    Orchestrates the Actor-Critic workflow for generating, reviewing, and revising drafts.
    """

    def __init__(self, topic: str, num_cycles: int):
        self.topic = topic
        self.num_cycles = num_cycles
        self.history_manager = HistoryManager()
        self.draft_manager = DraftManager(topic)

    def run(self) -> str:
        """
        Execute the Actor-Critic pipeline for the specified number of cycles.
        
        Returns:
            str: The final history in Markdown format.
        """
        for cycle in range(self.num_cycles):
            if cycle == 0:
                self.run_initial_cycle(cycle)
            else:
                self.run_revised_cycle(cycle)

        return self.history_manager.to_markdown()

    def run_initial_cycle(self, cycle: int) -> None:
        """
        Run the initial cycle of draft generation and review.
        
        Args:
            cycle (int): The current cycle number.
        """
        initial_draft = self.draft_manager.generate_initial_draft()
        self.history_manager.add_entry(f"Initial Draft v{cycle}", initial_draft)
        
        initial_review = self.draft_manager.review_draft(initial_draft)
        self.history_manager.add_entry("Initial Review", initial_review)

    def run_revised_cycle(self, cycle: int) -> None:
        """
        Run a revised cycle of draft revision and review.
        
        Args:
            cycle (int): The current cycle number.
        """
        revised_draft = self.draft_manager.revise_draft(self.history_manager.history_md)
        self.history_manager.add_entry(f"Revised Draft v{cycle}", revised_draft)
        
        revised_review = self.draft_manager.revise_review(self.history_manager.history_md)
        self.history_manager.add_entry(f"Revised Review v{cycle}", revised_review)


if __name__ == "__main__":
    topic = 'perplexity'
    num_cycles = 3

    try:
        pipeline = ActorCriticPipeline(topic=topic, num_cycles=num_cycles)
        final_history = pipeline.run()
        logger.info("Actor-Critic pipeline completed successfully.")
        print(final_history)
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
