import asyncio
from coordinator import CoordinatorAgent
from message import Message
from src.config.logging import logger

async def pipeline():
    # Initialize the coordinator agent
    coordinator = CoordinatorAgent(name="CoordinatorAgent")

    # Read the document content from the file
    with open('./data/patterns/parallel_task_decomposition/sample_doc.txt', 'r') as file:
        document_content = file.read()

    # Define the task input (document content)
    task_input = document_content

    # Create the message with the task input
    message = Message(content=task_input, sender="User", recipient="CoordinatorAgent")

    # Process the message and get the final result (async call to CoordinatorAgent)
    response = await coordinator.process(message)
    print('====> ', response.content, '======')

    # Save the extracted information to a file
    with open('./data/patterns/parallel_task_decomposition/extracted_info.txt', 'w') as output_file:
        output_file.write(response.content)

    # Print the final extracted result
    print("Extraction completed. The extracted information has been saved to 'extracted_info.txt'.")

if __name__ == "__main__":
    # Run the pipeline to process the document
    asyncio.run(pipeline())

