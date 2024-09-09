
from src.patterns.coordinator_delegate.message import Message
from src.patterns.coordinator_delegate.agent import Agent
from src.config.logging import logger 
from src.llm.generate import ResponseGenerator
from src.prompt.manage import TemplateManager


class FlightAgent(Agent):
    def process(self, message: Message) -> Message:
        logger.info(f"Flight Agent processing: {message.content}")
        template_manager = TemplateManager('./config/patterns/coordinate_delegate.yml')
        template = template_manager.create_template('delegate', 'flight_search')
        try:
            response = self.llm_client.get_response(prompt)
            return Message(response, self.name, "TravelPlannerAgent")
        except Exception as e:
            logger.error(f"Error in Flight Agent: {e}")
            return Message("I apologize, but I couldn't process the flight information at this time.", self.name, "TravelPlannerAgent")

class HotelAgent(Agent):
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

class CarRentalAgent(Agent):
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
