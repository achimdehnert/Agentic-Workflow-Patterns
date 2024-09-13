from src.patterns.coordinator_delegate.delegates.car_rental_search import CarRentalSearchAgent
from src.patterns.coordinator_delegate.delegates.flight_search import FlightSearchAgent
from src.patterns.coordinator_delegate.delegates.hotel_search import HotelSearchAgent
from src.patterns.coordinator_delegate.coordinator import TravelPlannerAgent
from src.patterns.coordinator_delegate.message import Message
from src.config.logging import logger

def main():
    # Initialize sub-agents
    flight_agent = FlightSearchAgent(name="FlightSearchAgent")
    hotel_agent = HotelSearchAgent(name="HotelSearchAgent")
    car_rental_agent = CarRentalSearchAgent(name="CarRentalSearchAgent")

    # Instantiate the TravelPlannerAgent with sub-agents
    travel_planner = TravelPlannerAgent(
        name="TravelPlannerAgent",
        sub_agents=[flight_agent, hotel_agent, car_rental_agent]
    )

    # Test queries
    queries = [
        "I want to book a flight from Miami to Dallas next week.",
        "Can you find me a hotel in Frisco, Texas for next week?",
        "I need a rental car in Frisco, Texas for a week."
    ]

    # Process each query
    for query in queries:
        try:
            message = Message(content=query, sender="User", recipient="TravelPlannerAgent")
            response_message = travel_planner.process(message)
            
            logger.info(f"Query: {query}")
            logger.info(f"Response: {response_message.content}")
            
            print(f"\nQuery: {query}")
            print(f"Response: {response_message.content}")
            print("-" * 50)
        
        except Exception as e:
            logger.error(f"Error processing query '{query}': {e}")
            print(f"\nError processing query '{query}': {e}")

if __name__ == '__main__':
    main()