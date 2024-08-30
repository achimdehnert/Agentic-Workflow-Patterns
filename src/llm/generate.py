from src.llm.strategy import GenerationStrategyFactory
from src.llm.factory import ModelFactoryProvider
from src.config.logging import logger
from src.config.setup import config
from typing import List
from typing import Dict 
from typing import Any 


class ResponseGenerator:
    def __init__(self, strategy_type: str = "default"):
        logger.info(f"Initializing ResponseGenerator with strategy_type: {strategy_type}")
        self.model_factory = ModelFactoryProvider.get_instance()
        logger.info("ModelFactoryProvider instance created successfully.")
        self.generation_strategy = GenerationStrategyFactory.get_strategy(strategy_type)
        logger.info(f"Generation strategy '{strategy_type}' selected.")

    def generate_response(self, system_instruction: str, contents: List[str], response_schema: Dict[str, Any]) -> Any:
        logger.info("Starting response generation.")
        
        try:
            logger.info(f"Creating model with name: {config.TEXT_GEN_MODEL_NAME}")
            model = self.model_factory.create_model(config.TEXT_GEN_MODEL_NAME, system_instruction)
            logger.info("Model created successfully.")
            
            generation_config = self.generation_strategy.create_generation_config(response_schema)
            safety_settings = self.generation_strategy.create_safety_settings()
            
            response = model.generate_content(contents, 
                                              generation_config=generation_config, 
                                              safety_settings=safety_settings)
            logger.info("Response generated successfully.")
            return response.text.strip()
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise