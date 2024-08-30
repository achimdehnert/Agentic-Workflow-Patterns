from vertexai.generative_models import GenerativeModel
from src.config.logging import logger
from abc import abstractmethod
from abc import ABC


class ModelFactory(ABC):
    @abstractmethod
    def create_model(self, model_name: str, system_instruction: str) -> GenerativeModel:
        raise NotImplementedError("Subclasses must implement the `create_model` method")

class VertexAIModelFactory(ModelFactory):
    def create_model(self, model_name: str, system_instruction: str) -> GenerativeModel:
        try:
            return GenerativeModel(model_name, system_instruction=system_instruction)
        except Exception as e:
            logger.error(f"Error creating GenerativeModel: {e}")
            raise


# Singleton pattern
class ModelFactoryProvider:
    _instance = None

    @staticmethod
    def get_instance() -> ModelFactory:
        if ModelFactoryProvider._instance is None:
            ModelFactoryProvider._instance = VertexAIModelFactory()
        return ModelFactoryProvider._instance