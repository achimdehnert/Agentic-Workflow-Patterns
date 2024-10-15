from src.config.logging import logger 
from typing import Any 
import json 
import os 


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