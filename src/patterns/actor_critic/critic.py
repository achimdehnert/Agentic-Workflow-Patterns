from src.patterns.actor_critic.agent import Agent, ContentGenerator
from src.config.logging import logger 

class DraftReviewGenerator(ContentGenerator):
    def generate(self, template_manager, response_generator, draft: str) -> str:
        template = template_manager.create_template('critic', 'review')
        system_instruction = template['system']
        user_instruction = template_manager.fill_template(template['user'], article=draft)
        return response_generator.generate_response(system_instruction, [user_instruction], template['schema'])

class ReviewRevisionGenerator(ContentGenerator):
    def generate(self, template_manager, response_generator, state: str) -> str:
        template = template_manager.create_template('critic', 'revise')
        system_instruction = template['system']
        user_instruction = template_manager.fill_template(template['user'], history=state)
        return response_generator.generate_response(system_instruction, [user_instruction], template['schema'])

class Critic(Agent):
    def review_draft(self, draft: str) -> str:
        try:
            review = self._generate_content(DraftReviewGenerator(), draft=draft)
            self._save_content(review, "feedback", 0)
            return review
        except Exception as e:
            logger.error(f"Error reviewing draft: {e}")
            raise

    def revise_review(self, state: str, version: int) -> str:
        try:
            revised_review = self._generate_content(ReviewRevisionGenerator(), state=state)
            self._save_content(revised_review, "feedback", version)
            return revised_review
        except Exception as e:
            logger.error(f"Error revising review: {e}")
            raise