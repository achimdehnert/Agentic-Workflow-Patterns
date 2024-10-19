from src.config.logging import logger 
from json import JSONDecodeError
from typing import Optional
from typing import Dict 
from typing import Any 
import json 
import re 


def extract_json_from_response(response_text: str) -> Optional[Dict[str, Any]]:
    """
    Extracts JSON content from a response text using a regular expression.

    Args:
        response_text (str): The text containing JSON wrapped in <JSON>...</JSON> tags.

    Returns:
        Optional[Dict[str, Any]]: Extracted JSON data as a dictionary, or None if extraction fails.
    """
    try:
        json_match = re.search(r'<JSON>(.*?)</JSON>', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1).strip()
            return json.loads(json_str)
        else:
            logger.error("No JSON content found in LLM response.")
            return None
    except JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
        return None