from src.patterns.coordinator_delegate.message import Message
from src.patterns.coordinator_delegate.agent import Agent
from patterns.web_search.pipeline import run
from src.config.logging import logger
from typing import Dict, Any
import json


class HotelSearchAgent(Agent):
    """
    Agent responsible for handling hotel search queries. It generates a query for web search and returns summarized results.
    """

    def process(self, message: Message) -> Message:
        """
        Processes hotel search queries by generating a web search query and returning summarized results.

        :param message: The incoming message containing the hotel query.
        :return: A response message with the hotel search results or an error message.
        """
        logger.info(f"{self.name} processing message: {message.content}")
        query = message.content
        try:
            template: Dict[str, Any] = self.template_manager.create_template('delegate', 'hotel_search')
            system_instructions: str = template['system']
            response_schema: Dict[str, Any] = template['schema']
            user_instructions: str = self.template_manager.fill_template(template['user'], query=query)
            contents = [user_instructions]

            logger.info(f"Generating response for hotel query: {query}")
            response = self.response_generator.generate_response(
                'gemini-1.5-pro-001', system_instructions, contents, response_schema)
            
            try:
                out_dict: Dict[str, Any] = json.loads(response.text.strip())
            except json.JSONDecodeError as decode_error:
                raise ValueError(f"Failed to decode JSON: {decode_error}")
            
            web_search_query: str = out_dict.get('web_search_query', '')
            if not web_search_query:
                raise ValueError("Web search query missing from the response.")

            logger.info(f"Running web search for query: {web_search_query}")
            web_search_results_summary: str = run(web_search_query)
            return Message(content=web_search_results_summary, sender=self.name, recipient="TravelPlannerAgent")

        except Exception as e:
            logger.error(f"Error in HotelSearchAgent: {e}")
            return Message(content="I apologize, but I couldn't process the hotel information at this time.", 
                           sender=self.name, recipient="TravelPlannerAgent")