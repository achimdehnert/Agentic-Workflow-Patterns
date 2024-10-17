from src.patterns.coordinator_delegate.message import Message
from src.patterns.coordinator_delegate.agent import Agent
from src.patterns.web_search.pipeline import run
from src.config.logging import logger
from typing import Dict
from typing import Any 
import json 


class HotelSearchAgent(Agent):
    async def process(self, message: Message) -> Message:
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
                'gemini-1.5-flash-001', system_instructions, contents, response_schema)
            
            out_dict: Dict[str, Any] = json.loads(response.text.strip())
            web_search_query: str = out_dict.get('web_search_query', '')
            if not web_search_query:
                raise ValueError("Web search query missing from the response.")

            logger.info(f"Running web search for query: {web_search_query}")
            web_search_results_summary: str = run(web_search_query)
            return Message(content=web_search_results_summary, sender=self.name, recipient="TravelPlannerAgent", metadata={"entity_type": "HOTEL"})

        except Exception as e:
            logger.error(f"Error in HotelSearchAgent: {e}")
            return Message(content="I apologize, but I couldn't process the hotel information at this time.", 
                           sender=self.name, recipient="TravelPlannerAgent", metadata={"entity_type": "HOTEL"})
