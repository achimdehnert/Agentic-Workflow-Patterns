from src.patterns.task_decomposition.message import Message

class Agent:
    """
    A base class for agents in the system.

    Attributes:
        name (str): The name of the agent.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes the Agent.

        Args:
            name (str): The name of the agent.
        """
        self.name = name

    async def process(self, message: 'Message') -> 'Message':
        """
        Processes a message.

        Args:
            message (Message): The message to process.

        Returns:
            Message: The response message.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")
