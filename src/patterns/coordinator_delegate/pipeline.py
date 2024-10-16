from typing import Union, List
from src.patterns.coordinator_delegate.delegates.car_rental_search import CarRentalSearchAgent
from src.patterns.coordinator_delegate.delegates.flight_search import FlightSearchAgent
from src.patterns.coordinator_delegate.delegates.hotel_search import HotelSearchAgent
from src.patterns.coordinator_delegate.coordinator import TravelPlannerAgent
from src.patterns.coordinator_delegate.message import Message
from src.config.logging import logger

class Pipeline:
    def __init__(self):
        # Initialize sub-agents
        self.flight_search_agent = FlightSearchAgent(name="FlightSearchAgent")
        self.hotel_search_agent = HotelSearchAgent(name="HotelSearchAgent")
        self.car_rental_search_agent = CarRentalSearchAgent(name="CarRentalSearchAgent")
        
        # Instantiate the TravelPlannerAgent with sub-agents
        self.travel_planner = TravelPlannerAgent(
            name="TravelPlannerAgent",
            sub_agents=[self.flight_search_agent, self.hotel_search_agent, self.car_rental_search_agent]
        )

    def execute(self, queries: Union[str, List[str]]) -> None:
        if isinstance(queries, str):
            queries = [queries]
        
        for query in queries:
            try:
                message = Message(content=query, sender="User", recipient="TravelPlannerAgent")
                response_message = self.travel_planner.process(message)
                
                logger.info(f"Query: {query}")
                logger.info(f"Response: {response_message.content}")
                
                print(f"\nQuery: {query}")
                print(f"Response: {response_message.content}")
                print("-" * 50)
            
            except Exception as e:
                logger.error(f"Error processing query '{query}': {e}")
                print(f"\nError processing query '{query}': {e}")

def run(queries: Union[str, List[str]]) -> None:
    # Create Pipeline instance and execute queries
    pipeline = Pipeline()
    pipeline.execute(queries)

if __name__ == '__main__':
    # Test queries
    test_queries = [
        "I want to book a flight from Miami to Dallas next week.",
        # "Can you find me a hotel in Frisco, Texas for next week?",
        # "I need a rental car in Frisco, Texas for a week."
    ]
    
    # Run the pipeline with test queries
    run(test_queries)
    
    # Example of running with a single query
    run("Could you recommend some hotels in Coimbatore, India for a stay next week?")