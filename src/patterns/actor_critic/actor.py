from src.llm.generate import ResponseGenerator
from src.prompt.manage import TemplateManager
from src.utils.io import save_to_file
from src.config.logging import logger
import yaml

class Actor:
    def __init__(self, topic: str):
        self.topic = topic
        self.response_generator = ResponseGenerator()
        self.template_manager = TemplateManager()

    def generate_initial_draft(self) -> str:
        try:
            system_instruction = self.template_manager.load_and_fill_template(
                './data/patterns/actor_critic/actor/draft/system_instructions.txt', 
                topic=self.topic
            )
            user_instruction = self.template_manager.load_and_fill_template(
                './data/patterns/actor_critic/actor/draft/user_instructions.txt', 
                topic=self.topic
            )
            with open('./data/patterns/actor_critic/actor/draft/response_schema.yaml', 'r') as f:
                response_schema = yaml.safe_load(f)

            draft = self.response_generator.generate_response(
                system_instruction, [user_instruction], response_schema
            )
            save_to_file(draft, "draft", 0)
            return draft['article']
        except Exception as e:
            logger.error(f"Error generating initial draft: {e}")
            raise

    def revise_draft(self, history: str, version: int) -> str:
        try:
            system_instruction = self.template_manager.load_template(
                './data/patterns/actor_critic/actor/revise/system_instructions.txt'
            )
            user_instruction = self.template_manager.load_and_fill_template(
                './data/patterns/actor_critic/actor/revise/user_instructions.txt', 
                history=history
            )
            with open('./data/patterns/actor_critic/actor/revise/response_schema.yaml', 'r') as f:
                response_schema = yaml.safe_load(f)

            revised_draft = self.response_generator.generate_response(
                system_instruction, [user_instruction], response_schema
            )
            save_to_file(revised_draft, "draft", version)
            return revised_draft['article']
        except Exception as e:
            logger.error(f"Error revising draft: {e}")
            raise