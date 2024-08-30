from src.config.logging import logger
from src.utils.io import load_json
from src.utils.io import load_yaml
from typing import Dict


class TemplateManager:
    def __init__(self, config_path: str):
        self.config = load_yaml(config_path)

    def create_template(self, role: str, action: str) -> Dict[str, str]:
        try:
            template_config = self.config[role][action]
            return {
                'system': self.load_template(template_config['system_instructions']),
                'user': self.load_template(template_config['user_instructions']),
                'schema': load_json(template_config['response_schema'])
            }
        except KeyError as e:
            logger.error(f"Invalid role or action in template configuration: {e}")
            raise
        except Exception as e:
            logger.error(f"Error creating template: {e}")
            raise

    @staticmethod
    def load_template(template_path: str) -> str:
        try:
            with open(template_path, 'r') as file:
                return file.read()
        except FileNotFoundError as e:
            logger.error(f"Template file not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading template: {e}")
            raise

    @staticmethod
    def fill_template(template_content: str, **kwargs) -> str:
        try:
            filled_template = template_content
            for key, value in kwargs.items():
                placeholder = f"{{{key}}}"
                filled_template = filled_template.replace(placeholder, str(value))
            return filled_template
        except Exception as e:
            logger.error(f"Error filling template: {e}")
            raise