from src.config.logging import logger
from abc import abstractmethod
from abc import ABC


class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass

class LogObserver(Observer):
    def update(self, message: str):
        logger.info(message)

class ProgressObserver(Observer):
    def update(self, message: str):
        print(f"Progress: {message}")
