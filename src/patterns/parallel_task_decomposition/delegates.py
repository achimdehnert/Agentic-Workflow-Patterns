from src.patterns.parallel_task_decomposition.agent import Agent
from src.patterns.parallel_task_decomposition.message import Message
from src.llm.generate import GenerationResponse
from src.config.logging import logger 

class SubTaskAgent(Agent):
    """
    An agent that processes a specific subtask of the document extraction
    by invoking an LLM to extract the required information.

    Attributes:
        name (str): The name of the subtask agent.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes the SubTaskAgent.

        Args:
            name (str): The name of the agent.
        """
        super().__init__(name)
        logger.info(f"{self.name} initialized.")

    async def process(self, message: Message) -> Message:
        """
        Processes the assigned subtask of the document by calling the LLM.

        Args:
            message (Message): The incoming message containing the subtask and document.

        Returns:
            Message: A message containing the result of the subtask from the LLM.
        """
        logger.info(f"{self.name} processing subtask.")
        subtask = message.content

        # Extract the document and task from the subtask
        document = subtask.get("document")
        task = subtask.get("task")

        if not document or not task:
            return Message(content="Invalid subtask: Missing document or task.", sender=self.name, recipient=message.sender)

        # Call the LLM using the generate method to perform the extraction
        llm_input = f"Document:\n{document}\n\nTask: {task}"
        logger.info(f"Calling LLM for task: {task}")
        
        try:
            # Call the LLM to perform the extraction based on the task
            extraction_result = generate(prompt=llm_input)
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            extraction_result = f"Failed to extract information for task: {task}"

        # Return the extraction result as a message
        return Message(content=extraction_result, sender=self.name, recipient=message.sender)
