from src.patterns.dynamic_task_decomposition.coordinator import CoordinatorAgent
from src.commons.message import Message
from src.config.logging import logger
import asyncio


async def pipeline() -> None:
    """
    The main pipeline that coordinates the processing of a book by invoking the CoordinatorAgent.
    
    This function reads the book content, creates a message, sends it to the CoordinatorAgent,
    and saves the final analysis summary to a file.
    """
    # Initialize the coordinator agent
    coordinator = CoordinatorAgent(name="CoordinatorAgent")

    # Read the book content from a file
    with open('./data/patterns/dynamic_task_decomposition/book.txt', 'r') as file:
        book_content = file.read()

    # Create the message containing the book content
    message = Message(content=book_content, sender="User", recipient="CoordinatorAgent")

    # Process the message and obtain the final result (asynchronously handled by CoordinatorAgent)
    response = await coordinator.process(message)

    # Save the final summary to a file
    with open('./data/patterns/dynamic_task_decomposition/book_analysis_summary.md', 'w') as output_file:
        output_file.write(response.content)

    # Log and print the completion message
    logger.info("Analysis completed. The summary has been saved to 'book_analysis_summary.md'.")
    print("Analysis completed. The summary has been saved to 'book_analysis_summary.md'.")


if __name__ == "__main__":
    # Run the pipeline to process the book
    asyncio.run(pipeline())
