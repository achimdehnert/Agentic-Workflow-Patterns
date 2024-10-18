from src.patterns.dynamic_task_decomposition.coordinator import CoordinatorAgent
from src.patterns.dynamic_task_decomposition.message import Message
from src.config.logging import logger
import asyncio


async def pipeline():
    # Initialize the coordinator agent
    coordinator = CoordinatorAgent(name="CoordinatorAgent")

    # Read the book content from the file
    with open('./data/patterns/dynamic_task_decomposition/book.txt', 'r') as file:
        book_content = file.read()

    # Create the message with the book content
    message = Message(content=book_content, sender="User", recipient="CoordinatorAgent")

    # Process the message and get the final result (async call to CoordinatorAgent)
    response = await coordinator.process(message)

    # Save the final summary to a file
    with open('./book_analysis_summary.md', 'w') as output_file:
        output_file.write(response.content)

    # Print the final result
    print("Analysis completed. The summary has been saved to 'book_analysis_summary.md'.")

if __name__ == "__main__":
    # Run the pipeline to process the book
    asyncio.run(pipeline())
