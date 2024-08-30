from src.patterns.actor_critic.agent import Agent, ContentGenerator
from src.config.logging import logger

class DraftGenerator(ContentGenerator):
    def generate(self, template_manager, response_generator, topic: str) -> str:
        template = template_manager.create_template('actor', 'draft')
        system_instruction = template_manager.fill_template(template['system'], topic=topic)
        user_instruction = template_manager.fill_template(template['user'], topic=topic)
        return response_generator.generate_response(system_instruction, [user_instruction], template['schema'])

class RevisionGenerator(ContentGenerator):
    def generate(self, template_manager, response_generator, state: str) -> str:
        template = template_manager.create_template('actor', 'revise')
        system_instruction = template['system']
        user_instruction = template_manager.fill_template(template['user'], history=state)
        return response_generator.generate_response(system_instruction, [user_instruction], template['schema'])

class Actor(Agent):
    def generate_initial_draft(self) -> str:
        try:
            draft = self._generate_content(DraftGenerator(), topic=self.topic)
            self._save_content(draft, "draft", 0)
            return draft
        except Exception as e:
            logger.error(f"Error generating initial draft: {e}")
            raise

    def revise_draft(self, state: str, version: int) -> str:
        try:
            revised_draft = self._generate_content(RevisionGenerator(), state=state)
            self._save_content(revised_draft, "draft", version)
            return revised_draft
        except Exception as e:
            logger.error(f"Error revising draft: {e}")
            raise