from src.llm.generate import ResponseGenerator
from src.prompt.manage import TemplateManager
from src.config.logging import logger
from src.utils.io import save_to_file
import yaml


class Critic:
    def __init__(self, topic: str):
        self.topic = topic
        self.response_generator = ResponseGenerator()
        self.template_manager = TemplateManager()

    def review_draft(self, draft: str) -> str:
        try:
            system_instruction = self.template_manager.load_template(
                './data/patterns/actor_critic/critic/review/system_instructions.txt'
            )
            user_instruction = self.template_manager.load_and_fill_template(
                './data/patterns/actor_critic/critic/review/user_instructions.txt', 
                article=draft
            )
            with open('./data/patterns/actor_critic/critic/review/response_schema.json', 'r') as f:
                response_schema = yaml.safe_load(f)

            review = self.response_generator.generate_response(
                system_instruction, [user_instruction], response_schema
            )
            save_to_file(review, "feedback", 0)
            return review
        except Exception as e:
            logger.error(f"Error reviewing draft: {e}")
            raise

    def revise_review(self, history: str, version: int) -> str:
        try:
            system_instruction = self.template_manager.load_template(
                './data/patterns/actor_critic/critic/revise/system_instructions.txt'
            )
            user_instruction = self.template_manager.load_and_fill_template(
                './data/patterns/actor_critic/critic/revise/user_instructions.txt', 
                history=history
            )
            with open('./data/patterns/actor_critic/critic/revise/response_schema.yaml', 'r') as f:
                response_schema = yaml.safe_load(f)

            revised_review = self.response_generator.generate_response(
                system_instruction, [user_instruction], response_schema
            )
            save_to_file(revised_review, "feedback", version)
            return revised_review
        except Exception as e:
            logger.error(f"Error revising review: {e}")
            raise