import asyncio
from src.patterns.parallel_task_decomposition.coordinator import CoordinatorAgent
from message import Message
import logging
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    # Initialize the coordinator agent
    coordinator = CoordinatorAgent(name="CoordinatorAgent")

    # Generate sample data
    np.random.seed(0)
    data = np.random.randn(1000)

    # Define the task input
    task_input = {
        'data': data
    }

    # Create the message with the task input
    message = Message(content=task_input, sender="User", recipient="CoordinatorAgent")

    # Process the message and get the final result
    response = await coordinator.process(message)

    # Print the final result
    print("Final Analysis Report:\n")
    print(response.content)


if __name__ == "__main__":
    asyncio.run(main())
