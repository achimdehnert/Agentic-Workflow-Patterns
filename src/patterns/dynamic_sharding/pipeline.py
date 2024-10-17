from src.patterns.dynamic_sharding.coordinator import Coordinator
from src.patterns.dynamic_sharding.message import Message
from src.config.logging import logger
import asyncio
import os

INPUT_FILE = "./data/patterns/dynamic_sharding/entities.txt"
OUTPUT_FILE = "./data/patterns/dynamic_sharding/entity_info.txt"

async def main():
    # Initialize the coordinator agent
    coordinator = Coordinator(name="CoordinatorAgent")

    # Read entities from the input file
    with open(INPUT_FILE, 'r') as f:
        entities = [line.strip() for line in f.readlines()]

    shard_size = 3  # Number of entities per shard

    # Create the message with the list and shard size
    message_content = {
        'entities': entities,
        'shard_size': shard_size
    }
    message = Message(content=message_content, sender="User", recipient="CoordinatorAgent")

    # Process the message and get the consolidated information
    response = await coordinator.process(message)

    # Save the final consolidated response to the output file
    with open(OUTPUT_FILE, 'w') as f:
        f.write(response.content)

    print(f"Entity information has been saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    # Configure logging
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Run the main function
    asyncio.run(main())