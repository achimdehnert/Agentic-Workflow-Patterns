from src.patterns.coordinator_delegate.message import Message

from src.patterns.coordinator_delegate.agent import Agent

from src.llm.generate import ResponseGenerator
from src.prompt.manage import TemplateManager
from src.patterns.web_search.run import run 

from src.config.logging import logger 


template_manager = TemplateManager('./config/patterns/coordinator_delegate.yml')
response_generator = ResponseGenerator()

class FlightSearchAgent(Agent):
    def process(self, message: Message) -> Message:
        logger.info(f"Flight Agent processing: {message.content}")
        query = message.content
        template = template_manager.create_template('delegate', 'flight_search')
        system_instructions = template['system']
        response_schema = template['schema']
        user_instructions = template_manager.fill_template(template['user'], query=query)
        contents = [user_instructions]
        try:
            response = response_generator.generate_response('gemini-1.5-pro-001', system_instructions, contents, response_schema)
            out_dict = response.text.strip()
            web_search_query = eval(out_dict)['web_search_query']
            web_search_results_summary = run(web_search_query)
            return Message(web_search_results_summary, self.name, "TravelPlannerAgent")
        except Exception as e:
            logger.error(f"Error in Flight Agent: {e}")
            return Message("I apologize, but I couldn't process the flight information at this time.", self.name, "TravelPlannerAgent")

class HotelSearchAgent(Agent):
    def process(self, message: Message) -> Message:
        logger.info(f"Hotel Agent processing: {message.content}")
        prompt = f"""As a hotel booking assistant, provide a detailed response to the following query. Include suggestions for hotels, price ranges, and any relevant local information.

Query: {message.content}

Response:"""
        try:
            response = self.llm_client.get_response(prompt)
            return Message(response, self.name, "TravelPlannerAgent")
        except Exception as e:
            logger.error(f"Error in Hotel Agent: {e}")
            return Message("I apologize, but I couldn't process the hotel information at this time.", self.name, "TravelPlannerAgent")

class CarRentalSearchAgent(Agent):
    def process(self, message: Message) -> Message:
        logger.info(f"Car Rental Agent processing: {message.content}")
        prompt = f"""As a car rental assistant, provide a detailed response to the following query. Include suggestions for car rental companies, estimated prices, and any relevant travel tips.

Query: {message.content}

Response:"""
        try:
            response = self.llm_client.get_response(prompt)
            return Message(response, self.name, "TravelPlannerAgent")
        except Exception as e:
            logger.error(f"Error in Car Rental Agent: {e}")
            return Message("I apologize, but I couldn't process the car rental information at this time.", self.name, "TravelPlannerAgent")
