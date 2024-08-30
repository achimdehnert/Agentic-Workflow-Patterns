from src.llm.generate import ResponseGenerator
from src.prompt.manage import TemplateManager
from src.utils.io import save_to_disk
from src.config.logging import logger
from abc import ABC, abstractmethod


class ReviewGenerator(ABC):
    @abstractmethod
    def generate(self, **kwargs) -> str:
        pass

class DraftReviewGenerator(ReviewGenerator):
    def generate(self, template_manager: TemplateManager, response_generator: ResponseGenerator, draft: str) -> str:
        template = template_manager.create_template('critic', 'review')
        system_instruction = template['system']
        user_instruction = template_manager.fill_template(template['user'], article=draft)
        return response_generator.generate_response(system_instruction, [user_instruction], template['schema'])

class ReviewRevisionGenerator(ReviewGenerator):
    def generate(self, template_manager: TemplateManager, response_generator: ResponseGenerator, history: str) -> str:
        template = template_manager.create_template('critic', 'revise')
        system_instruction = template['system']
        user_instruction = template_manager.fill_template(template['user'], history=history)
        return response_generator.generate_response(system_instruction, [user_instruction], template['schema'])

class Critic:
    def __init__(self, topic: str, config_path: str, output_path: str,):
        self.topic = topic
        self.output_path = output_path
        
        self.template_manager = TemplateManager(config_path)
        self.response_generator = ResponseGenerator()
        

    def _generate_review(self, generator: ReviewGenerator, **kwargs) -> str:
        return generator.generate(template_manager=self.template_manager, 
                                  response_generator=self.response_generator, 
                                  **kwargs)

    def review_draft(self, draft: str) -> str:
        try:
            review = self._generate_review(DraftReviewGenerator(), draft=draft)
            save_to_disk(review, "feedback", 0, self.output_path)
            return review
        except Exception as e:
            logger.error(f"Error reviewing draft: {e}")
            raise

    def revise_review(self, history: str, version: int) -> str:
        try:
            revised_review = self._generate_review(ReviewRevisionGenerator(), history=history)
            save_to_disk(revised_review, "feedback", version, self.output_path)
            return revised_review
        except Exception as e:
            logger.error(f"Error revising review: {e}")
            raise