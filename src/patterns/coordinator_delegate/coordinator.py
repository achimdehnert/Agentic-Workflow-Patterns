
from src.patterns.coordinator_delegate.message import Message
from src.patterns.coordinator_delegate.agent import Agent
from src.config.logging import logger 
from typing import List 
from enum import Enum


class Intent(Enum):
    FLIGHT = 1
    HOTEL = 2
    CAR_RENTAL = 3
    UNKNOWN = 4


class TravelPlannerAgent(Agent):
    """
    # Master Agent (now renamed to TravelPlannerAgent) which routes requests to the appropriate sub-agent
    """
    def __init__(self, name: str, sub_agents: List[Agent], llm_client: LLMClient):
        super().__init__(name, llm_client)
        self.sub_agents = {agent.name: agent for agent in sub_agents}

    def determine_intent(self, query: str) -> Intent:
        prompt = f"""Determine the primary intent of the following travel-related query. Respond with only one word: FLIGHT, HOTEL, or CAR_RENTAL.

Query: {query}

Intent:"""
        try:
            response = self.llm_client.get_response(prompt)
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
            final_response = self.llm_client.get_response(consolidation_prompt)
            return Message(final_response, self.name, "User")
        except Exception as e:
            logger.error(f"Error consolidating response: {e}")
            return Message("I apologize, but I encountered an error while processing your request. Please try again later.", self.name, "User")