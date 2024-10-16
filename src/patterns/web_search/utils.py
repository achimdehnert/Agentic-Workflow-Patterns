from src.config.logging import logger 
import hashlib


def generate_filename(query: str) -> str:
    """
    Generate a unique filename based on the provided query string.

    Args:
        query (str): The query string for which a unique filename is generated.

    Returns:
        str: A unique filename in the format '<md5_hash>.json'.
    """
    try:
        encoded_query = query.encode('utf-8')
        filename = f"{hashlib.md5(encoded_query).hexdigest()}.json"
        return filename
    except Exception as e:
        logger.error(f"Error generating filename for query '{query}': {e}")
        raise
