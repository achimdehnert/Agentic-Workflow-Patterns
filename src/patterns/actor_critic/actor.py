from src.llm.generate import ResponseGenerator
from src.prompt.manage import TemplateManager
from src.utils.io import save_to_disk
from src.config.logging import logger
from abc import abstractmethod
from typing import Any 
from abc import ABC


class ContentGenerator(ABC):
    """
    Abstract base class for content generation. All subclasses must implement the `generate` method.
    """
    
    @abstractmethod
    def generate(self, **kwargs: Any) -> str:
        """
        Generate content based on provided arguments.

        Args:
            **kwargs: Arbitrary keyword arguments required by the specific generator.

        Returns:
            str: The generated content.
        """
        raise NotImplementedError("Subclasses must implement the `generate` method")


class DraftGenerator(ContentGenerator):
    """
    Generates the initial draft content using the specified template and response generator.
    """

    def generate(self, template_manager: TemplateManager, response_generator: ResponseGenerator, topic: str) -> str:
        """
        Generate the initial draft based on the given topic.

        Args:
            template_manager (TemplateManager): Manages the templates.
            response_generator (ResponseGenerator): Generates responses based on instructions.
            topic (str): The topic for which the draft is generated.

        Returns:
            str: The generated initial draft.
        """
        template = template_manager.create_template('actor', 'draft')
        system_instruction = template_manager.fill_template(template['system'], topic=topic)
        user_instruction = template_manager.fill_template(template['user'], topic=topic)
        return response_generator.generate_response(system_instruction, [user_instruction], template['schema'])


class RevisionGenerator(ContentGenerator):
    """
    Generates a revised draft content based on the provided history.
    """

    def generate(self, template_manager: TemplateManager, response_generator: ResponseGenerator, state: str) -> str:
        """
        Generate a revised draft based on the given history.

        Args:
            template_manager (TemplateManager): Manages the templates.
            response_generator (ResponseGenerator): Generates responses based on instructions.
            state (str): The current state or history to be used for revision.

        Returns:
            str: The generated revised draft.
        """
        template = template_manager.create_template('actor', 'revise')
        system_instruction = template['system']
        user_instruction = template_manager.fill_template(template['user'], history=state)
        return response_generator.generate_response(system_instruction, [user_instruction], template['schema'])


class Actor:
    """
    Handles the generation of drafts and their revisions based on a given topic.
    """

    def __init__(self, topic: str, config_path: str, output_path: str):
        """
        Initialize the Actor with a topic, configuration path, and output path.

        Args:
            topic (str): The topic for generating content.
            config_path (str): Path to the configuration file.
            output_path (str): Path where the generated content will be saved.
        """
        self.topic = topic
        self.output_path = output_path
        self.template_manager = TemplateManager(config_path)
        self.response_generator = ResponseGenerator()

    def _generate_content(self, generator: ContentGenerator, **kwargs: Any) -> str:
        """
        Internal method to generate content using the provided generator.

        Args:
            generator (ContentGenerator): An instance of a content generator.
            **kwargs: Additional arguments required by the generator.

        Returns:
            str: The generated content.
        """
        return generator.generate(template_manager=self.template_manager, 
                                  response_generator=self.response_generator, 
                                  **kwargs)

    def generate_initial_draft(self) -> str:
        """
        Generate the initial draft for the given topic and save it to disk.

        Returns:
            str: The generated initial draft.

        Raises:
            Exception: If an error occurs during draft generation.
        """
        try:
            draft = self._generate_content(DraftGenerator(), topic=self.topic)
            save_to_disk(draft, "draft", 0, self.output_path)
            return draft
        except Exception as e:
            logger.error(f"Error generating initial draft: {e}")
            raise

    def revise_draft(self, state: str, version: int) -> str:
        """
        Revise the existing draft based on the provided state and save the revised version to disk.

        Args:
            state (str): The current state or history of the draft.
            version (int): The version number of the draft.

        Returns:
            str: The revised draft.

        Raises:
            Exception: If an error occurs during draft revision.
        """
        try:
            revised_draft = self._generate_content(RevisionGenerator(), state=state)
            save_to_disk(revised_draft, "draft", version, self.output_path)
            return revised_draft
        except Exception as e:
            logger.error(f"Error revising draft: {e}")
            raise
