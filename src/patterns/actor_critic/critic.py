from src.llm.generate import ResponseGenerator
from src.prompt.manage import TemplateManager
from src.utils.io import save_to_disk
from src.config.logging import logger
from abc import abstractmethod
from typing import Any 
from abc import ABC


class ReviewGenerator(ABC):
    """
    Abstract base class for generating reviews. All subclasses must implement the `generate` method.
    """
    
    @abstractmethod
    def generate(self, **kwargs: Any) -> str:
        """
        Generate a review based on provided arguments.

        Args:
            **kwargs: Arbitrary keyword arguments required by the specific generator.

        Returns:
            str: The generated review.
        """
        pass


class DraftReviewGenerator(ReviewGenerator):
    """
    Generates a review for an initial draft using the specified template and response generator.
    """

    def generate(self, template_manager: TemplateManager, response_generator: ResponseGenerator, draft: str) -> str:
        """
        Generate a review for the given draft.

        Args:
            template_manager (TemplateManager): Manages the templates.
            response_generator (ResponseGenerator): Generates responses based on instructions.
            draft (str): The draft content to be reviewed.

        Returns:
            str: The generated review.
        """
        template = template_manager.create_template('critic', 'review')
        system_instruction = template['system']
        user_instruction = template_manager.fill_template(template['user'], article=draft)
        return response_generator.generate_response(system_instruction, [user_instruction], template['schema'])


class ReviewRevisionGenerator(ReviewGenerator):
    """
    Generates a revised review based on the provided history.
    """

    def generate(self, template_manager: TemplateManager, response_generator: ResponseGenerator, state: str) -> str:
        """
        Generate a revised review based on the given history.

        Args:
            template_manager (TemplateManager): Manages the templates.
            response_generator (ResponseGenerator): Generates responses based on instructions.
            state (str): The current state or history to be used for the review revision.

        Returns:
            str: The generated revised review.
        """
        template = template_manager.create_template('critic', 'revise')
        system_instruction = template['system']
        user_instruction = template_manager.fill_template(template['user'], history=state)
        return response_generator.generate_response(system_instruction, [user_instruction], template['schema'])


class Critic:
    """
    Handles the generation of reviews and their revisions based on a given topic.
    """

    def __init__(self, topic: str, config_path: str, output_path: str):
        """
        Initialize the Critic with a topic, configuration path, and output path.

        Args:
            topic (str): The topic for generating reviews.
            config_path (str): Path to the configuration file.
            output_path (str): Path where the generated reviews will be saved.
        """
        self.topic = topic
        self.output_path = output_path
        self.template_manager = TemplateManager(config_path)
        self.response_generator = ResponseGenerator()

    def _generate_review(self, generator: ReviewGenerator, **kwargs: Any) -> str:
        """
        Internal method to generate a review using the provided generator.

        Args:
            generator (ReviewGenerator): An instance of a review generator.
            **kwargs: Additional arguments required by the generator.

        Returns:
            str: The generated review.
        """
        return generator.generate(template_manager=self.template_manager, 
                                  response_generator=self.response_generator, 
                                  **kwargs)

    def review_draft(self, draft: str) -> str:
        """
        Generate a review for the initial draft and save it to disk.

        Args:
            draft (str): The draft content to be reviewed.

        Returns:
            str: The generated review.

        Raises:
            Exception: If an error occurs during review generation.
        """
        try:
            review = self._generate_review(DraftReviewGenerator(), draft=draft)
            save_to_disk(review, "feedback", 0, self.output_path)
            return review
        except Exception as e:
            logger.error(f"Error reviewing draft: {e}")
            raise

    def revise_review(self, state: str, version: int) -> str:
        """
        Revise the existing review based on the provided state and save the revised version to disk.

        Args:
            state (str): The current state or history of the review.
            version (int): The version number of the review.

        Returns:
            str: The revised review.

        Raises:
            Exception: If an error occurs during review revision.
        """
        try:
            revised_review = self._generate_review(ReviewRevisionGenerator(), state=state)
            save_to_disk(revised_review, "feedback", version, self.output_path)
            return revised_review
        except Exception as e:
            logger.error(f"Error revising review: {e}")
            raise
