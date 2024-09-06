from abc import abstractmethod
from src.patterns.coordinator_delegate.message import Message
from src.llm.generate import GenerationResponse
from abc import ABC


# Abstract base class for the agent
class Agent(ABC):
    def __init__(self, name: str, response_generator: GenerationResponse):
        self.name = name
        self.response_generator = response_generator

    @abstractmethod
    def process(self, message: Message) -> Message:
        pass