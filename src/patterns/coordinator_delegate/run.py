
from src.config.logging import logger 
from src.patterns.coordinator_delegate.delegates import HotelAgent
from src.patterns.coordinator_delegate.delegates import FlightAgent
from src.patterns.coordinator_delegate.delegates import CarRentalAgent
from src.patterns.coordinator_delegate.coordinator import TravelPlannerAgent
from src.patterns.coordinator_delegate.message import Message

class Pipeline:
    def __init__(self):
        # self.llm_client = LLMClient()  # Initialize the LLM client
        # Create sub-agents for each specific travel need
        sub_agents = [
            FlightAgent("FlightAgent", self.llm_client),
            HotelAgent("HotelAgent", self.llm_client),
            CarRentalAgent("CarRentalAgent", self.llm_client),
        ]
        # Initialize the main travel planner agent with the sub-agents
        self.travel_planner_agent = TravelPlannerAgent("TravelPlannerAgent", sub_agents, self.llm_client)

    def process_query(self, query: str) -> str:
        # Create a message object with the user's query
        initial_message = Message(query, "User", "TravelPlannerAgent")
        # Pass the message to the travel planner agent for processing
        final_message = self.travel_planner_agent.process(initial_message)
        # Return the final result from the agent's response
        return final_message.content

# Main function to handle the entire workflow
def main():
    # Initialize the travel planning workflow
    pipeline = Pipeline()
    
    # List of queries to be processed in the workflow
    queries = [
        "I need to book a flight from New York to London next month",
        "Find me a luxury hotel in Paris for a week-long stay",
        "I'm looking to rent a car in Los Angeles for a weekend",
        "I need suggestions for a beach vacation"
    ]
    
    # Iterate through each query and process it
    for query in queries:
        try:
            # Process the query using the workflow and get the result
            result = pipeline.process_query(query)
            print(f"Query: {query}")
            print(f"Result: {result}")
            print()
        except Exception as e:
            # Log any errors encountered during processing
            logger.error(f"Error processing query '{query}': {e}")

# Entry point for the script
if __name__ == "__main__":
    main()
