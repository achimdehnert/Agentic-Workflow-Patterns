from abc import abstractmethod
from src.patterns.coordinator_delegate.message import Message
from src.llm.generate import GenerationResponse
from abc import ABC


# Abstract base class for the agent
class Agent(ABC):
    def __init__(self, name: str, llm_client: GenerationResponse):
        self.name = name
        self.llm_client = llm_client

    @abstractmethod
    def process(self, message: Message) -> Message:
        pass