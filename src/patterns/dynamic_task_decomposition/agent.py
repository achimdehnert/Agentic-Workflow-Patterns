from src.patterns.task_decomposition.message import Message
from abc import ABC, abstractmethod

class Agent(ABC):
    """
    A base class for agents in the system.

    Attributes:
        name (str): The name of the agent.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes the Agent with a name.

        Args:
            name (str): The name of the agent.
        """
        self.name = name

    @abstractmethod
    async def process(self, message: 'Message') -> 'Message':
        """
        Abstract method to process a message. Must be implemented by subclasses.

        Args:
            message (Message): The message to be processed.

        Returns:
            Message: The response message after processing.
        """
        raise NotImplementedError("Subclasses must implement this method.")
