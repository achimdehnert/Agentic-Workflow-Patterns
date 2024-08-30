from src.llm.generate import ResponseGenerator
from src.prompt.manage import TemplateManager
from src.utils.io import save_to_disk
from src.config.logging import logger
from abc import ABC, abstractmethod


class ContentGenerator(ABC):
    @abstractmethod
    def generate(self, **kwargs) -> str:
        raise NotImplementedError("Subclasses must implement the `generate` method")


class DraftGenerator(ContentGenerator):
    def generate(self, template_manager: TemplateManager, response_generator: ResponseGenerator, topic: str) -> str:
        template = template_manager.create_template('actor', 'draft')
        system_instruction = template_manager.fill_template(template['system'], topic=topic)
        user_instruction = template_manager.fill_template(template['user'], topic=topic)
        return response_generator.generate_response(system_instruction, [user_instruction], template['schema'])


class RevisionGenerator(ContentGenerator):
    def generate(self, template_manager: TemplateManager, response_generator: ResponseGenerator, history: str) -> str:
        template = template_manager.create_template('actor', 'revise')
        system_instruction = template['system']
        user_instruction = template_manager.fill_template(template['user'], history=history)
        return response_generator.generate_response(system_instruction, [user_instruction], template['schema'])


class Actor:
    def __init__(self, topic: str, config_path: str, output_path: str,):
        self.topic = topic
        self.output_path = output_path

        self.template_manager = TemplateManager(config_path)
        self.response_generator = ResponseGenerator()
        

    def _generate_content(self, generator: ContentGenerator, **kwargs) -> str:
        return generator.generate(template_manager=self.template_manager, 
                                  response_generator=self.response_generator, 
                                  **kwargs)

    def generate_initial_draft(self) -> str:
        try:
            draft = self._generate_content(DraftGenerator(), topic=self.topic)
            save_to_disk(draft, "draft", 0, self.output_path)
            return draft
        except Exception as e:
            logger.error(f"Error generating initial draft: {e}")
            raise

    def revise_draft(self, history: str, version: int) -> str:
        try:
            revised_draft = self._generate_content(RevisionGenerator(), history=history)
            save_to_disk(revised_draft, "draft", version, self.output_path)
            return revised_draft
        except Exception as e:
            logger.error(f"Error revising draft: {e}")
            raise