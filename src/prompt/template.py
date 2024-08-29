from src.config.logging import logger


def load_template(template_path: str) -> str:
    """
    Load a template from a file.

    Args:
        template_path (str): The path to the template file.

    Returns:
        str: The content of the template as a string.
    """
    try:
        with open(template_path, 'r') as file:
            return file.read()
    except FileNotFoundError as e:
        logger.error(f"Template file not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading template: {e}")
        raise


def fill_template(template_content: str, **kwargs) -> str:
    """
    Replace placeholders in the template content with the provided keyword arguments.

    Args:
        template_content (str): The content of the template.
        kwargs: Key-value pairs where the key is the placeholder name and the value is the content to replace it with.

    Returns:
        str: The filled template as a string.
    """
    try:
        filled_template = template_content
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            filled_template = filled_template.replace(placeholder, value)
        return filled_template
    except Exception as e:
        logger.error(f"Error filling template: {e}")
        raise


def load_and_fill_template(template_path: str, **kwargs) -> str:
    """
    Load a template from a file and replace placeholders with the provided keyword arguments.

    Args:
        template_path (str): The path to the template file.
        kwargs: Key-value pairs where the key is the placeholder name and the value is the content to replace it with.

    Returns:
        str: The filled template as a string.
    """
    try:
        template_content = load_template(template_path)
        return fill_template(template_content, **kwargs)
    except Exception as e:
        logger.error(f"Error loading and filling template: {e}")
        raise


if __name__ == "__main__":
    template_path = "./data/patterns/actor_critic/actor/draft/system_instructions.txt"
    topic = "perplexity"

    # Load and fill the template
    filled_template = load_and_fill_template(template_path, topic=topic)

    # Print the filled template
    print(filled_template)
