from src.patterns.coordinator_delegate.delegates import CarRentalSearchAgent, FlightSearchAgent, HotelSearchAgent
from src.patterns.coordinator_delegate.message import Message
from src.patterns.coordinator_delegate.agent import Agent
from src.config.logging import logger
from typing import List, Dict, Union
from enum import Enum


class Intent(Enum):
    """
    Enum to define possible user intents for travel planning.
    """
    FLIGHT = 1
    HOTEL = 2
    CAR_RENTAL = 3
    UNKNOWN = 4


class TravelPlannerAgent(Agent):
    """
    Travel Planner agent responsible for routing travel-related queries to sub-agents 
    based on detected intent and generating a consolidated response.
    """

    def __init__(self, name: str, sub_agents: List[Agent]) -> None:
        """
        Initializes the TravelPlannerAgent with a set of sub-agents and shared resources.

        :param name: Name of the agent.
        :param sub_agents: List of sub-agents responsible for specific tasks like flights, hotels, etc.
        """
        super().__init__(name)
        self.sub_agents: Dict[str, Agent] = {agent.name: agent for agent in sub_agents}
        logger.info(f"{self.name} initialized with {len(self.sub_agents)} sub-agents.")

    def determine_intent(self, query: str) -> Intent:
        """
        Determines the user's intent based on their query using a response generation model.

        :param query: User's query string.
        :return: Detected intent as an Intent enum value.
        """
        try:
            template = self.template_manager.create_template('coordinator', 'route')
            system_instructions = template['system']
            user_instructions = self.template_manager.fill_template(template['user'], query=query)
            response_schema = template['schema']
            contents = [user_instructions]

            logger.info(f"Generating response to determine intent for query: {query}")
            response = self.response_generator.generate_response('gemini-1.5-pro-001', system_instructions, contents, response_schema)
            out_dict = eval(response.text.strip())  # Caution: Ensure safe eval usage
            intent_str = out_dict.get('intent', 'UNKNOWN').upper()
            logger.info(f"Determined intent: {intent_str}")
            return Intent[intent_str]

        except KeyError as e:
            logger.error(f"Key error while determining intent: {e}")
            return Intent.UNKNOWN
        except Exception as e:
            logger.error(f"Unexpected error while determining intent: {e}")
            return Intent.UNKNOWN

    def route_to_agent(self, intent: Intent) -> Union[Agent, None]:
        """
        Routes the query to the appropriate sub-agent based on the determined intent.

        :param intent: The user's detected intent.
        :return: The corresponding sub-agent for the intent or None if not applicable.
        """
        intent_to_agent = {
            Intent.FLIGHT: "FlightSearchAgent",
            Intent.HOTEL: "HotelSearchAgent",
            Intent.CAR_RENTAL: "CarRentalSearchAgent",
            Intent.UNKNOWN: None
        }

        agent_name = intent_to_agent.get(intent)
        if not agent_name:
            logger.error(f"No valid agent found for intent: {intent}")
            return None

        logger.info(f"Routing to agent: {agent_name}")
        return self.sub_agents.get(agent_name)

    def process(self, message: Message) -> Message:
        """
        Processes the incoming message, determines intent, routes to the appropriate sub-agent, 
        and returns a consolidated response.

        :param message: The incoming message to process.
        :return: A response message after processing by the sub-agent and consolidation.
        """
        logger.info(f"{self.name} processing message: {message.content}")
        
        try:
            query = message.content

            # Determine the user's intent
            intent = self.determine_intent(query)
            
            # Route to the appropriate sub-agent
            sub_agent = self.route_to_agent(intent)
            if sub_agent is None:
                raise ValueError(f"Unknown intent: {intent}")

            sub_message = Message(content=query, sender=self.name, recipient=sub_agent.name, metadata={"intent": intent.name})
            logger.info(f"Delegating message to {sub_agent.name}")

            # Get the response from the sub-agent
            sub_response = sub_agent.process(sub_message)
            summary = sub_response.content

            # Consolidate the final response
            template = self.template_manager.create_template('coordinator', 'consolidate')
            system_instructions = self.template_manager.fill_template(template['system'], query=query, summary=summary)
            user_instructions = self.template_manager.fill_template(template['user'], query=query, summary=summary)
            contents = [user_instructions]

            logger.info("Generating final response for the user.")
            final_response = self.response_generator.generate_response('gemini-1.5-pro-001', system_instructions, contents)
            final_response_text = final_response.text.strip()
            return Message(content=final_response_text, sender=self.name, recipient="User")

        except ValueError as e:
            logger.error(f"ValueError occurred: {e}")
            return Message(content="I'm sorry, I could not process your request. Please try again later.", sender=self.name, recipient="User")
        except Exception as e:
            logger.error(f"Unexpected error during processing: {e}")
            return Message(content="I encountered an error while processing your request. Please try again later.", sender=self.name, recipient="User")


if __name__ == '__main__':
    # Initialize sub-agents (Flight, Hotel, CarRental)
    flight_agent = FlightSearchAgent(name="FlightSearchAgent")
    hotel_agent = HotelSearchAgent(name="HotelSearchAgent")
    car_rental_agent = CarRentalSearchAgent(name="CarRentalSearchAgent")

    # Instantiate the TravelPlannerAgent with sub-agents
    travel_planner = TravelPlannerAgent(
        name="TravelPlannerAgent",
        sub_agents=[flight_agent, hotel_agent, car_rental_agent])
    """
    # Test case 1: Flight search
    user_flight_query = "I want to book a flight from Miami to Dallas  next week."
    flight_message = Message(content=user_flight_query, sender="User", recipient="TravelPlannerAgent")

    # Process the flight message using TravelPlannerAgent
    flight_response_message = travel_planner.process(flight_message)
    logger.info(f"Response to the flight query: {flight_response_message.content}")
    print("Flight Search Response:", flight_response_message.content)

    # Test case 2: Hotel search
    user_hotel_query = "Can you find me a hotel in Frisco, Texas for next week?"
    hotel_message = Message(content=user_hotel_query, sender="User", recipient="TravelPlannerAgent")

    # Process the hotel message using TravelPlannerAgent
    hotel_response_message = travel_planner.process(hotel_message)
    logger.info(f"Response to the hotel query: {hotel_response_message.content}")
    print("Hotel Search Response:", hotel_response_message.content)
    """
    # Test case 3: Car rental search
    user_car_rental_query = "I need a rental car in Frisco, Texas for a week."
    car_rental_message = Message(content=user_car_rental_query, sender="User", recipient="TravelPlannerAgent")

    # Process the car rental message using TravelPlannerAgent
    car_rental_response_message = travel_planner.process(car_rental_message)
    logger.info(f"Response to the car rental query: {car_rental_response_message.content}")
    print("Car Rental Search Response:", car_rental_response_message.content)
