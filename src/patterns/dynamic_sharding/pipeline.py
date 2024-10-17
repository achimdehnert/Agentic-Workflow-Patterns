
from src.patterns.dynamic_sharding.coordinator import CoordinatorAgent
from src.patterns.dynamic_sharding.message import Message
from src.config.logging import logger
import asyncio


async def main():
    # Initialize the coordinator agent
    coordinator = CoordinatorAgent(name="CoordinatorAgent")

    # Define the list of celebrity names and shard size
    celebrity_names = [
        "Leonardo DiCaprio",
        "Angelina Jolie",
        "Tom Cruise",
        "Scarlett Johansson",
        "Brad Pitt",
        "Jennifer Lawrence",
        "Johnny Depp",
        "Natalie Portman",
        "Will Smith",
        "Emma Watson"
    ]
    shard_size = 3  # Number of celebrities per shard

    # Create the message with the list and shard size
    message_content = {
        'celebrity_names': celebrity_names,
        'shard_size': shard_size
    }
    message = Message(content=message_content, sender="User", recipient="CoordinatorAgent")

    # Process the message and get the consolidated biographies
    response = await coordinator.process(message)

    # Print the final consolidated response
    print("Final Consolidated Biographies:\n")
    print(response.content)


if __name__ == "__main__":
    # Configure logging
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Run the main function
    asyncio.run(main())
