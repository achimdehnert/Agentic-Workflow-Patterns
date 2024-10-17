from src.patterns.web_search.pipeline import run as web_search
from src.patterns.coordinator_delegate.message import Message
from src.patterns.coordinator_delegate.agent import Agent
from src.config.logging import logger
from typing import Optional
import json


class CarRentalSearchAgent(Agent):
    """
    Agent responsible for handling car rental queries, generating a web search query, 
    and returning summarized results.
    """

    def process(self, message: Message) -> Message:
        """
        Processes car rental queries by generating a web search query and returning summarized results.

        :param message: The incoming message containing the car rental query.
        :return: A response message with the car rental search results or an error message.
        """
        logger.info(f"{self.name} processing message: '{message.content}'")
        query = message.content
        try:
            template = self.template_manager.create_template('delegate', 'car_rental_search')
            system_instructions = template.get('system', '')
            response_schema = template.get('schema', '')
            user_instructions = self.template_manager.fill_template(template.get('user', ''), query=query)
            contents = [user_instructions]

            logger.info(f"Generating response for car rental query: '{query}'")
            response = self.response_generator.generate_response(
                'gemini-1.5-flash-001', system_instructions, contents, response_schema
            )

            try:
                out_dict = json.loads(response.text.strip())
            except json.JSONDecodeError as decode_error:
                logger.error(f"Failed to decode JSON response: {decode_error}")
                return Message(
                    content="Error in parsing response. Please try again later.",
                    sender=self.name,
                    recipient="TravelPlannerAgent"
                )

            web_search_query: Optional[str] = out_dict.get('web_search_query')
            if not web_search_query:
                logger.warning("Web search query missing from the response.")
                return Message(
                    content="Unable to find relevant car rental information at this time.",
                    sender=self.name,
                    recipient="TravelPlannerAgent"
                )

            logger.info(f"Running web search for query: '{web_search_query}'")
            web_search_results_summary = web_search(web_search_query)
            return Message(content=web_search_results_summary, sender=self.name, recipient="TravelPlannerAgent")

        except Exception as e:
            logger.error(f"Error in CarRentalSearchAgent: {e}")
            return Message(
                content="I apologize, but I couldn't process the car rental information at this time.",
                sender=self.name,
                recipient="TravelPlannerAgent"
            )
