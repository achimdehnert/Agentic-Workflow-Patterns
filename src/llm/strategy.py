from vertexai.generative_models import HarmBlockThreshold 
from vertexai.generative_models import GenerationConfig
from vertexai.generative_models import HarmCategory
from src.config.logging import logger
from abc import abstractmethod
from typing import Dict
from typing import Any 
from abc import ABC


class GenerationStrategy(ABC):
    @abstractmethod
    def create_generation_config(self, response_schema: Dict[str, Any]) -> GenerationConfig:
        raise NotImplementedError("Subclasses must implement the `create_generation_config` method")

    @abstractmethod
    def create_safety_settings(self) -> Dict[HarmCategory, HarmBlockThreshold]:
        raise NotImplementedError("Subclasses must implement the `create_safety_settings` method")


class DefaultGenerationStrategy(GenerationStrategy):
    def create_generation_config(self, response_schema: Dict[str, Any]) -> GenerationConfig:
        try:
            return GenerationConfig(
                temperature=0.0,
                top_p=0.0,
                top_k=1,
                candidate_count=1,
                max_output_tokens=8192,
                response_mime_type="application/json",
                response_schema=response_schema
            )
        except Exception as e:
            logger.error(f"Error creating generation configuration: {e}")
            raise

    def create_safety_settings(self) -> Dict[HarmCategory, HarmBlockThreshold]:
        try:
            return {
                HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
            }
        except Exception as e:
            logger.error(f"Error creating safety settings: {e}")
            raise


# Factory method pattern
class GenerationStrategyFactory:
    @staticmethod
    def get_strategy(strategy_type: str = "default") -> GenerationStrategy:
        if strategy_type == "default":
            return DefaultGenerationStrategy()
        else:
            raise ValueError(f"Unknown strategy type: {strategy_type}")