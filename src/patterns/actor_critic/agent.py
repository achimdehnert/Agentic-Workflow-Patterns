from abc import ABC, abstractmethod
from typing import Any
from src.llm.generate import ResponseGenerator
from src.prompt.manage import TemplateManager
from src.utils.io import save_to_disk
from src.config.logging import logger


class ContentGenerator(ABC):
    @abstractmethod
    def generate(self, **kwargs: Any) -> str:
        raise NotImplementedError("Subclasses must implement the `generate` method")


class Agent:
    def __init__(self, topic: str, config_path: str, output_path: str):
        self.topic = topic
        self.output_path = output_path
        self.template_manager = TemplateManager(config_path)
        self.response_generator = ResponseGenerator()

    def _generate_content(self, generator: ContentGenerator, **kwargs: Any) -> str:
        return generator.generate(template_manager=self.template_manager, 
                                  response_generator=self.response_generator, 
                                  **kwargs)

    def _save_content(self, content: str, content_type: str, version: int) -> None:
        try:
            save_to_disk(content, content_type, version, self.output_path)
        except Exception as e:
            logger.error(f"Error saving {content_type}: {e}")
            raise