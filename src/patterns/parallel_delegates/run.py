from src.patterns.parallel_delegates.delegates.car_rental_search import CarRentalSearchAgent
from src.patterns.parallel_delegates.delegates.flight_search import FlightSearchAgent
from src.patterns.parallel_delegates.delegates.hotel_search import HotelSearchAgent
from src.config.logging import logger 

from src.patterns.parallel_delegates.agent import Agent
from src.patterns.parallel_delegates.message import Message
from src.patterns.parallel_delegates.coordinator import TravelPlannerAgent
import asyncio



async def main():
    # Initialize sub-agents
    flight_agent = FlightSearchAgent(name="FlightSearchAgent")
    hotel_agent = HotelSearchAgent(name="HotelSearchAgent")
    car_rental_agent = CarRentalSearchAgent(name="CarRentalSearchAgent")

    # Instantiate the TravelPlannerAgent with sub-agents
    travel_planner = TravelPlannerAgent(
        name="TravelPlannerAgent",
        sub_agents=[flight_agent, hotel_agent, car_rental_agent])

    # Test the travel planner
    user_query = "I need a flight from New York to Los Angeles, a hotel in downtown LA, and a rental car for next week."
    initial_message = Message(content=user_query, sender="User", recipient="TravelPlannerAgent")
    response = await travel_planner.process(initial_message)
    print(f"Travel Planner Response: {response.content}")

if __name__ == "__main__":
    asyncio.run(main())