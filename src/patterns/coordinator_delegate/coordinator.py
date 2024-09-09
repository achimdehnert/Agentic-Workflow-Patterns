from src.patterns.coordinator_delegate.delegates import FlightSearchAgent
from src.patterns.coordinator_delegate.message import Message
from src.patterns.coordinator_delegate.agent import Agent
from src.llm.generate import ResponseGenerator
from src.prompt.manage import TemplateManager
from src.config.logging import logger 
from typing import List, Dict
from enum import Enum

from src.patterns.web_search.run import run


class Intent(Enum):
    FLIGHT = 1
    HOTEL = 2
    CAR_RENTAL = 3
    UNKNOWN = 4


class TravelPlannerAgent(Agent):
    """
    Coordinator agent responsible for routing travel-related queries to the appropriate sub-agent
    based on the detected intent. It consolidates and generates user-friendly responses using
    a response generator and predefined templates.
    """

    def __init__(self, name: str, sub_agents: List[Agent], response_generator: ResponseGenerator):
        """
        Initializes the TravelPlannerAgent with the provided sub-agents and response generator.

        :param name: Name of the agent.
        :param sub_agents: List of sub-agents responsible for specific tasks like flight, hotel, car rental, etc.
        :param response_generator: The generator used for generating responses from models.
        """
        super().__init__(name, response_generator)
        self.sub_agents: Dict[str, Agent] = {agent.name: agent for agent in sub_agents}
        self.response_generator = response_generator
        self.template_manager = TemplateManager('./config/patterns/coordinator_delegate.yml')
        logger.info(f"{self.name} initialized with {len(self.sub_agents)} sub-agents.")

    def determine_intent(self, query: str) -> Intent:
        """
        Determines the user's intent based on their query using a response generation model.

        :param query: The user's query.
        :return: The determined intent as an `Intent` enum.
        """
        try:
            template = self.template_manager.create_template('coordinator', 'travel_planner')
            system_instructions = template['system']
            user_instructions = self.template_manager.fill_template(template['user'], query=query)
            response_schema = template['schema']
            contents = [user_instructions]

            logger.info(f"Generating response to determine intent for query: {query}")
            response = self.response_generator.generate_response('gemini-1.5-pro-001', system_instructions, contents, response_schema)
            out_dict = eval(response.text.strip())  # Caution: Ensure safe eval usage
            intent = out_dict['intent'].upper()
            logger.info(f"Determined intent: {intent}")
            return Intent[intent]

        except KeyError as e:
            logger.error(f"Key error while determining intent: {e}")
            return Intent.UNKNOWN
        except Exception as e:
            logger.error(f"Unexpected error while determining intent: {e}")
            return Intent.UNKNOWN

    def route_to_agent(self, intent: Intent) -> Agent:
        """
        Routes the query to the appropriate sub-agent based on the determined intent.

        :param intent: The user's determined intent.
        :return: The agent responsible for handling that intent.
        """
        intent_to_agent = {
            Intent.FLIGHT: "FlightSearchAgent",
            Intent.HOTEL: "HotelSearchAgent",
            Intent.CAR_RENTAL: "CarRentalSearchAgent",
            Intent.UNKNOWN: "Not Applicable"
        }

        agent_name = intent_to_agent.get(intent, "Not Applicable")
        print(agent_name)
        if agent_name == "Not Applicable":
            logger.error(f"No valid agent found for intent: {intent}")
            raise ValueError(f"Unknown intent: {intent}")

        logger.info(f"Routing to agent: {agent_name}")
        return self.sub_agents[agent_name]

    def process(self, message: Message) -> Message:
        """
        Processes the incoming message by determining intent and routing to the appropriate sub-agent.

        :param message: The incoming message to be processed.
        :return: A response message consolidated from the sub-agent's response.
        """
        logger.info(f"{self.name} processing message: {message.content}")
        
        try:
            # Determine intent
            intent = self.determine_intent(message.content)
            
            # Route to the appropriate sub-agent
            sub_agent = self.route_to_agent(intent)
            print(sub_agent)
            sub_message = Message(content=message.content, sender=self.name, recipient=sub_agent.name, metadata={"intent": intent.name})
            
            # Process message with the sub-agent
            logger.info(f"Delegating message to {sub_agent.name}")
            response = sub_agent.process(sub_message)

            # Consolidate and generate the final response
            consolidation_prompt = f"""Consolidate the following travel information into a coherent response:

            Original Query: {message.content}
            Agent Response: {response.content}

            Provide a friendly and informative response to the user:"""

            logger.info("Generating final response to user.")
            final_response_text = self.response_generator.generate_response(consolidation_prompt).strip()
            return Message(content=final_response_text, sender=self.name, recipient="User")

        except ValueError as e:
            logger.error(f"ValueError occurred: {e}")
            return Message(content="I'm sorry, I could not process your request. Please try again later.", sender=self.name, recipient="User")
        except Exception as e:
            logger.error(f"Unexpected error during processing: {e}")
            return Message(content="I apologize, but I encountered an error while processing your request. Please try again later.", sender=self.name, recipient="User")


if __name__ == '__main__':
    # Initialize sub-agents (Flight, Hotel, CarRental) and the response generator
    flight_agent = FlightSearchAgent(name="FlightSearchAgent", response_generator=ResponseGenerator())

    # Instantiate the TravelPlannerAgent with sub-agents
    travel_planner = TravelPlannerAgent(
        name="TravelPlannerAgent", 
        sub_agents=[flight_agent], 
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
