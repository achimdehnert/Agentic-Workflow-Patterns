from src.config.logging import logger
from typing import Any, Dict
import yaml
import os


def load_yaml(filename: str) -> Dict[str, Any]:
    try:
        with open(filename, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logger.error(f"File '{filename}' not found.")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file '{filename}': {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading YAML file: {e}")
        raise


def save_to_file(content: Any, content_type: str, version: int) -> None:
    try:
        base_path = "./data/patterns/actor_critic/output"
        directory = os.path.join(base_path, content_type)
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, f"v{version}.yaml")

        with open(file_path, "w") as file:
            yaml.dump(content, file)

        logger.info(f"Saved {content_type} v{version} to {file_path}")
    except Exception as e:
        logger.error(f"Failed to save {content_type} v{version}: {e}")
        raise