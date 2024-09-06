

from src.patterns.coordinator_delegate.message import Message
from src.patterns.coordinator_delegate.agent import Agent
from src.llm.generate import ResponseGenerator
from src.config.logging import logger 
from typing import List 
from enum import Enum
from src.patterns.coordinator_delegate.delegates import FlightAgent

class Intent(Enum):
    FLIGHT = 1
    HOTEL = 2
    CAR_RENTAL = 3
    UNKNOWN = 4


class TravelPlannerAgent(Agent):
    """
    # Coordinator agent which routes requests to the appropriate sub-agent
    """
    def __init__(self, name: str, sub_agents: List[Agent], response_generator: ResponseGenerator):
        super().__init__(name, response_generator)
        self.sub_agents = {agent.name: agent for agent in sub_agents}
        self.response_generator = response_generator

    def determine_intent(self, query: str) -> Intent:
        prompt = f"""Determine the primary intent of the following travel-related query. Respond with only one word: FLIGHT, HOTEL, or CAR_RENTAL.

Query: {query}

Intent:"""
        try:
            response = self.response_generator.generate_response(prompt)
            return Intent[response.strip().upper()]
        except Exception as e:
            logger.error(f"Error determining intent: {e}")
            return Intent.UNKNOWN

    def route_to_agent(self, intent: Intent) -> Agent:
        intent_to_agent = {
            Intent.FLIGHT: "FlightAgent",
            Intent.HOTEL: "HotelAgent",
            Intent.CAR_RENTAL: "CarRentalAgent",
            Intent.UNKNOWN: "GeneralAgent"
        }
        return self.sub_agents[intent_to_agent[intent]]

    def process(self, message: Message) -> Message:
        logger.info(f"TravelPlannerAgent processing: {message.content}")
        intent = self.determine_intent(message.content)
        sub_agent = self.route_to_agent(intent)
        sub_message = Message(message.content, self.name, sub_agent.name, {"intent": intent.name})
        response = sub_agent.process(sub_message)
        
        consolidation_prompt = f"""Consolidate the following travel information into a coherent response:

Original Query: {message.content}
Agent Response: {response.content}

Provide a friendly and informative response to the user:"""
        
        try:
            final_response = self.response_generator.generate_response(consolidation_prompt)
            return Message(final_response, self.name, "User")
        except Exception as e:
            logger.error(f"Error consolidating response: {e}")
            return Message("I apologize, but I encountered an error while processing your request. Please try again later.", self.name, "User")
        

if __name__ == '__main__':
    # Initialize sub-agents (Flight, Hotel, CarRental) and the response generator
    flight_agent = FlightAgent(name="FlightAgent", response_generator=ResponseGenerator())

    # Instantiate the TravelPlannerAgent with sub-agents
    travel_planner = TravelPlannerAgent(
        name="TravelPlanner",
        sub_agents=[flight_agent, flight_agent],
        response_generator=ResponseGenerator()
    )

    # Simulate a user query (for example, asking for a flight)
    user_query = "I want to book a flight from New York to Los Angeles next week."
    message = Message(content=user_query, sender="User", recipient="TravelPlannerAgent")

    # Process the message using TravelPlannerAgent
    response_message = travel_planner.process(message)

    # Output the response
    logger.info(f"Response to the user: {response_message.content}")
    print(response_message.content)

