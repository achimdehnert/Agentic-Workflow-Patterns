from src.config.logging import logger
from typing import Optional
from typing import Dict 
from typing import Any 
import json 
import yaml
import os


def load_yaml(filename: str) -> Dict[str, Any]:
    """
    Load a YAML file and return its contents.

    Args:
        filename (str): The path to the YAML file.

    Returns:
        Dict[str, Any]: The parsed YAML object.

    Raises:
        FileNotFoundError: If the file is not found.
        yaml.YAMLError: If there is an error parsing the YAML file.
        Exception: For any other exceptions.
    """
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


def load_json(filename: str) -> Optional[Dict[str, Any]]:
    """
    Load a JSON file and return its contents.

    Args:
        filename (str): The path to the JSON file.

    Returns:
        Optional[Dict[str, Any]]: The parsed JSON object, or None if an error occurs.

    Raises:
        FileNotFoundError: If the file is not found.
        json.JSONDecodeError: If there is an error parsing the JSON file.
        Exception: For any other exceptions.
    """
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"File '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        logger.error(f"File '{filename}' contains invalid JSON.")
        return None
    except Exception as e:
        logger.error(f"Error loading JSON file: {e}")
        raise


def save_to_disk(content: Any, content_type: str, version: int, output_path: str) -> None:
    """
    Save the given content to a file with a specified version in the appropriate directory.

    The method determines the directory based on the `content_type` and saves the file with a 
    name formatted as "v{version}.txt". If the content is a dictionary, it is converted to 
    a formatted JSON string before saving.

    Args:
        content (Any): The content to save. If it is a dictionary, it will be converted to 
                       a JSON-formatted string.
        content_type (str): The type of content, either 'draft' or 'feedback', which determines 
                            the subdirectory where the file will be saved.
        version (int): The version number used in the filename (e.g., 'v1.txt').
        output_path (str): The base path where the directory and file will be created.

    Raises:
        Exception: If an error occurs during the file saving process, the exception is logged 
                   and re-raised.
    """
    try:
        directory = os.path.join(output_path, content_type)
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, f"v{version}.json")

        if isinstance(content, dict):
            content = json.dumps(content, indent=4)  # Convert dict to a formatted string

        with open(file_path, "w") as file:
            file.write(content)

        logger.info(f"Saved {content_type} v{version} to {file_path}")
    except Exception as e:
        logger.error(f"Failed to save {content_type} v{version}: {e}")
        raise

