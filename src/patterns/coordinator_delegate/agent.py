from src.patterns.coordinator_delegate.message import Message
from src.llm.generate import GenerationResponse
from abc import abstractmethod
from abc import ABC


class Agent(ABC):
    """
    Abstract base class for agents that handle specific tasks in a coordinator-delegate pattern.
    Each agent must implement the 'process' method to handle incoming messages.
    """

    def __init__(self, name: str, response_generator: GenerationResponse) -> None:
        """
        Initializes the Agent with a name and a response generator.

        :param name: Name of the agent.
        :param response_generator: An instance of the response generator used to handle message responses.
        """
        self.name: str = name
        self.response_generator: GenerationResponse = response_generator
        logger.info(f"Agent {self.name} initialized with response generator.")

    @abstractmethod
    def process(self, message: Message) -> Message:
        """
        Abstract method to process the incoming message. Must be implemented by subclasses.

        :param message: The message to be processed by the agent.
        :raise NotImplementedError: If the method is not implemented by a subclass.
        :return: A processed Message object with the response.
        """
        raise NotImplementedError(f"{self.__class__.__name__} has not implemented the 'process' method.")