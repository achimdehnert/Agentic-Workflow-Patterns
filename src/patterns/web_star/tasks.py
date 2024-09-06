from abc import abstractmethod
from abc import ABC


class SearchTask(ABC):
    @abstractmethod
    def run(self, model_name: str, query: str) -> None:
        raise NotImplementedError("Subclasses must implement the `run` method")
    

class ScrapeTask(ABC):
    @abstractmethod
    def run(self, model_name: str, query: str) -> None:
        raise NotImplementedError("Subclasses must implement the `run` method")
    

class SummarizeTask(ABC):
    @abstractmethod
    def run(self, model_name: str, query: str) -> None:
        raise NotImplementedError("Subclasses must implement the `run` method")