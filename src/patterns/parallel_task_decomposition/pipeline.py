from src.patterns.parallel_task_decomposition.coordinator import CoordinatorAgent  
from src.patterns.parallel_task_decomposition.message import Message 
from src.config.logging import logger 
import asyncio


async def pipeline():
    # Initialize the coordinator agent
    coordinator = CoordinatorAgent(name="CoordinatorAgent")

    # Example document input for extraction
    document_content = """
    This is an example document that needs to be processed. It contains multiple sections such as terms, conditions, dates, 
    parties involved, obligations, and other important legal clauses that need to be extracted.
    """

    # Define the task input (document content)
    task_input = document_content

    # Create the message with the task input
    message = Message(content=task_input, sender="User", recipient="CoordinatorAgent")

    # Process the message and get the final result (async call to CoordinatorAgent)
    response = await coordinator.process(message)

    # Print the final extracted result
    print("Final Extracted Document Summary:\n")
    print(response.content)

if __name__ == "__main__":
    # Run the pipeline to process the document
    asyncio.run(pipeline())
