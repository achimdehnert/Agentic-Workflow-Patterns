import abc
import logging
from typing import List, Dict, Optional
from enum import Enum
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define travel-related intents using the Enum design pattern
class Intent(Enum):
    FLIGHT = 1
    HOTEL = 2
    CAR_RENTAL = 3
    UNKNOWN = 4

# Define a message structure using a class
class Message:
    def __init__(self, content: str, sender: str, recipient: str, metadata: Optional[Dict] = None):
        self.content = content
        self.sender = sender
        self.recipient = recipient
        self.metadata = metadata or {}

# Define the LLM client for handling communication with an external API
class LLMClient:
    def __init__(self):
        pass

    def get_response(self, prompt: str) -> str:
        return 'Mock response'

# Abstract base class for the agent
class Agent(abc.ABC):
    def __init__(self, name: str, llm_client: LLMClient):
        self.name = name
        self.llm_client = llm_client

    @abc.abstractmethod
    def process(self, message: Message) -> Message:
        pass

# Master Agent (now renamed to TravelPlannerAgent) which routes requests to the appropriate sub-agent
class TravelPlannerAgent(Agent):
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

# Define the specific agents for flights, hotels, and car rentals
class FlightAgent(Agent):
    def process(self, message: Message) -> Message:
        logger.info(f"Flight Agent processing: {message.content}")
        prompt = f"""As a flight booking assistant, provide a detailed response to the following query. Include suggestions for airlines, estimated prices, and any relevant travel tips.

Query: {message.content}

Response:"""
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

class GeneralAgent(Agent):
    def process(self, message: Message) -> Message:
        logger.info(f"General Agent processing: {message.content}")
        prompt = f"""As a general travel assistant, provide a helpful response to the following query. Offer general travel advice and suggestions.

Query: {message.content}

Response:"""
        try:
            response = self.llm_client.get_response(prompt)
            return Message(response, self.name, "TravelPlannerAgent")
        except Exception as e:
            logger.error(f"Error in General Agent: {e}")
            return Message("I apologize, but I couldn't process your request at this time.", self.name, "TravelPlannerAgent")

# Workflow class to handle the entire process
class TravelPlanningWorkflow:
    def __init__(self):
        self.llm_client = LLMClient()
        sub_agents = [
            FlightAgent("FlightAgent", self.llm_client),
            HotelAgent("HotelAgent", self.llm_client),
            CarRentalAgent("CarRentalAgent", self.llm_client),
            GeneralAgent("GeneralAgent", self.llm_client)
        ]
        self.travel_planner_agent = TravelPlannerAgent("TravelPlannerAgent", sub_agents, self.llm_client)

    def process_query(self, query: str) -> str:
        initial_message = Message(query, "User", "TravelPlannerAgent")
        final_message = self.travel_planner_agent.process(initial_message)
        return final_message.content

# Entry point for the workflow
def main():
    workflow = TravelPlanningWorkflow()
    queries = [
        "I need to book a flight from New York to London next month",
        "Find me a luxury hotel in Paris for a week-long stay",
        "I'm looking to rent a car in Los Angeles for a weekend",
        "I need suggestions for a beach vacation"
    ]
    
    for query in queries:
        try:
            result = workflow.process_query(query)
            print(f"Query: {query}")
            print(f"Result: {result}")
            print()
        except Exception as e:
            logger.error(f"Error processing query '{query}': {e}")

if __name__ == "__main__":
    main()
