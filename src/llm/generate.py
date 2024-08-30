from src.llm.strategy import GenerationStrategyFactory
from src.llm.factory import ModelFactoryProvider
from src.config.logging import logger
from src.config.setup import config
from typing import List
from typing import Dict 
from typing import Any 
import yaml


class ResponseGenerator:
    def __init__(self, strategy_type: str = "default"):
        self.model_factory = ModelFactoryProvider.get_instance()
        self.generation_strategy = GenerationStrategyFactory.get_strategy(strategy_type)

    def generate_response(self, system_instruction: str, contents: List[str], response_schema: Dict[str, Any]) -> Any:
        try:
            model = self.model_factory.create_model(config.TEXT_GEN_MODEL_NAME, system_instruction)
            response = model.generate_content(contents, 
                                              generation_config=self.generation_strategy.create_generation_config(response_schema), 
                                              safety_settings=self.generation_strategy.create_safety_settings())
            return yaml.safe_load(response.text.strip())
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML response: {e}")
            raise
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise