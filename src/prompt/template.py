
from src.config.logging import logger
from typing import Optional
from typing import Dict 
from typing import Any 
import json 


def load_template(template_path):
    with open(template_path, 'r') as file:
        template_content = file.read()
    return template_content


def load_and_fill_template(template_path: str, topic: str) -> str:
    """
    Load a template from a file and replace all occurrences of {} with the topic.

    Args:
        template_path (str): The path to the template file.
        topic (str): The AI concept to insert into the template.

    Returns:
        str: The filled template as a string.
    """
    try:
        with open(template_path, 'r') as file:
            template_content = file.read()
            # logger.info(f"Loaded template content: {template_content}")
            
            # Replace all occurrences of '{}' with the topic
            filled_template = template_content.replace("{topic}", topic)
            
            # logger.info(f"Filled template content: {filled_template}")
            return filled_template
    except FileNotFoundError as e:
        logger.error(f"Template file not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading and filling template: {e}")
        raise


def load_and_fill_template2(template_path: str, article: str) -> str:
    """
    Load a template from a file and replace all occurrences of {} with the topic.

    Args:
        template_path (str): The path to the template file.
        topic (str): The AI concept to insert into the template.

    Returns:
        str: The filled template as a string.
    """
    try:
        with open(template_path, 'r') as file:
            template_content = file.read()
            #logger.info(f"Loaded template content: {template_content}")
            
            # Replace all occurrences of '{}' with the topic
            filled_template = template_content.replace("{article}", article)
            
            #logger.info(f"Filled template content: {filled_template}")
            return filled_template
    except FileNotFoundError as e:
        logger.error(f"Template file not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading and filling template: {e}")
        raise



def load_and_fill_template3(template_path: str, history: str) -> str:
    """
    Load a template from a file and replace all occurrences of {} with the topic.

    Args:
        template_path (str): The path to the template file.
        topic (str): The AI concept to insert into the template.

    Returns:
        str: The filled template as a string.
    """
    try:
        with open(template_path, 'r') as file:
            template_content = file.read()
            #logger.info(f"Loaded template content: {template_content}")
            
            # Replace all occurrences of '{}' with the topic
            filled_template = template_content.replace("{history}", history)
            
            #logger.info(f"Filled template content: {filled_template}")
            return filled_template
    except FileNotFoundError as e:
        logger.error(f"Template file not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading and filling template: {e}")
        raise



def load_json(filename: str) -> Optional[Dict[str, Any]]:
    """
    Load a JSON file and return its contents.

    Args:
        filename (str): The path to the JSON file.

    Returns:
        Optional[Dict[str, Any]]: The parsed JSON object, or None if an error occurs.
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

