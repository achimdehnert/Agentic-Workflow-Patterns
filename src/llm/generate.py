from vertexai.generative_models import GenerationResponse
from src.llm.strategy import GenerationStrategyFactory
from src.llm.factory import ModelFactoryProvider
from src.config.logging import logger
from src.config.setup import config
from typing import Optional
from typing import List
from typing import Dict
from typing import Any


class ResponseGenerator:
    """
    A class to handle the generation of responses using different generation strategies
    and model factories. The strategy and model used can be customized by specifying
    the `strategy_type` in the configuration.

    Attributes:
        model_factory: An instance of ModelFactoryProvider to create model instances.
        generation_strategy: The selected strategy for content generation.
    """

    def __init__(self, strategy_type: str = "default") -> None:
        """
        Initializes the ResponseGenerator with the specified strategy type.

        Args:
            strategy_type (str): The type of strategy to use for content generation. Defaults to "default".
        """
        self.model_factory = ModelFactoryProvider.get_instance()
        self.generation_strategy = GenerationStrategyFactory.get_strategy(strategy_type)

    def generate_response(self, model_name: str, system_instruction: str, contents: List[str], response_schema: Optional[Dict[str, Any]] = None, tools: List[Any] = None) -> GenerationResponse:
        """
        Generates a response based on the provided model name, system instruction, contents, response schema, and tools.

        Args:
            model_name (str): The name of the model to be used for generation.
            system_instruction (str): The instruction or prompt provided to the model.
            contents (List[str]): A list of content strings that will be used as input for response generation.
            response_schema (Optional[Dict[str, Any]]): A schema that defines the structure and constraints of the generated response. Defaults to None.
            tools (List[Any]): A list of tools to be passed to the model for content generation. Defaults to None.

        Returns:
        --------
        GenerationResponse: The generated response object.

        Raises:
        -------
        Exception: If there is an error during the response generation process.
        """
        logger.info("Starting response generation.")
        
        try:
            logger.info(f"Creating model instance for: {model_name}")
            model = self.model_factory.create_model(model_name, system_instruction)
            logger.info("Model created successfully.")
            
            generation_config = self.generation_strategy.create_generation_config(response_schema) if response_schema else None
            safety_settings = self.generation_strategy.create_safety_settings()
            
            response = model.generate_content(
                contents, 
                generation_config=generation_config, 
                safety_settings=safety_settings,
                tools=tools
            )
            logger.info("Response generated successfully.")
            return response 
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
