from src.patterns.web_search.pipeline import run as web_search
from src.patterns.coordinator_delegate.message import Message
from src.patterns.coordinator_delegate.agent import Agent
from src.config.logging import logger
import json

class FlightSearchAgent(Agent):
    """
    Agent responsible for handling flight search queries. It generates a query for web search and returns summarized results.
    """

    def process(self, message):
        """
        Processes flight search queries by generating a web search query and returning summarized results.

        :param message: The incoming message containing the flight query.
        :return: A response message with the flight search results or an error message.
        """
        logger.info(f"{self.name} processing message: {message.content}")
        query = message.content
        try:
            template = self.template_manager.create_template('delegate', 'flight_search')
            system_instructions = template['system']
            response_schema = template['schema']
            user_instructions = self.template_manager.fill_template(template['user'], query=query)
            contents = [user_instructions]

            logger.info(f"Generating response for flight query: {query}")
            response = self.response_generator.generate_response(
                'gemini-1.5-flash-001', system_instructions, contents, response_schema)
            
            # Handle the response safely
            try:
                out_dict = json.loads(response.text.strip())
            except json.JSONDecodeError as decode_error:
                raise ValueError(f"Failed to decode JSON: {decode_error}")
            
            web_search_query = out_dict.get('web_search_query', '')
            if not web_search_query:
                raise ValueError("Web search query missing from the response.")

            logger.info(f"Running web search for query: {web_search_query}")
            web_search_results_summary = web_search(web_search_query)
            return Message(content=web_search_results_summary, sender=self.name, recipient="TravelPlannerAgent")

        except Exception as e:
            logger.error(f"Error in FlightSearchAgent: {e}")
            return Message(content="I apologize, but I couldn't process the flight information at this time.", 
                           sender=self.name, recipient="TravelPlannerAgent")