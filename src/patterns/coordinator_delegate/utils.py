from src.config.logging import logger
from datetime import datetime
from typing import Union
import json 
import os 


BASE_DIR = "./data/patterns/coordinator_delegates/output"

def ensure_directory_exists(path: str) -> None:
    """
    Ensure that the directory exists, creating it if it doesn't.
    
    :param path: The directory path to check or create.
    """
    try:
        os.makedirs(path, exist_ok=True)
        logger.info(f"Directory ensured at: {path}")
    except OSError as e:
        logger.error(f"Failed to create directory at {path}: {str(e)}")
        raise


def generate_filename(prefix: str, extension: str) -> str:
    """
    Generate a filename with the current timestamp.
    
    :param prefix: The prefix for the filename.
    :param extension: The file extension (e.g., 'json' or 'txt').
    :return: A string representing the generated filename.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"


def save_json_response(category: str, response_type: str, content: Union[dict, list]) -> None:
    """
    Save responses as JSON files.
    
    :param category: Either 'coordinator' or 'delegate'.
    :param response_type: The type of response (e.g., 'route', 'consolidate', or delegate name).
    :param content: The response content to save, must be serializable to JSON.
    """
    try:
        if category not in ['coordinator', 'delegate']:
            logger.error(f"Invalid category provided: {category}")
            raise ValueError("Invalid category. Must be 'coordinator' or 'delegate'")
        
        dir_path = os.path.join(BASE_DIR, category)
        if category == 'coordinator':
            dir_path = os.path.join(dir_path, response_type)
        
        ensure_directory_exists(dir_path)

        filename = generate_filename(response_type, 'json')
        file_path = os.path.join(dir_path, filename)

        with open(file_path, 'w') as f:
            json.dump(content, f, indent=2)
        
        logger.info(f"Saved {category} {response_type} response as JSON to {file_path}")
    except (OSError, ValueError, TypeError) as e:
        logger.error(f"Failed to save JSON response: {str(e)}")
        raise


def save_text_response(category: str, response_type: str, content: str) -> None:
    """
    Save responses as text files.
    
    :param category: Either 'coordinator' or 'delegate'.
    :param response_type: The type of response (e.g., 'route', 'consolidate', or delegate name).
    :param content: The response content to save as text.
    """
    try:
        if category not in ['coordinator', 'delegate']:
            logger.error(f"Invalid category provided: {category}")
            raise ValueError("Invalid category. Must be 'coordinator' or 'delegate'")
        
        dir_path = os.path.join(BASE_DIR, category)
        if category == 'coordinator':
            dir_path = os.path.join(dir_path, response_type)
        
        ensure_directory_exists(dir_path)

        filename = generate_filename(response_type, 'txt')
        file_path = os.path.join(dir_path, filename)

        with open(file_path, 'w') as f:
            f.write(content)
        
        logger.info(f"Saved {category} {response_type} response as text to {file_path}")
    except (OSError, ValueError) as e:
        logger.error(f"Failed to save text response: {str(e)}")
        raise
