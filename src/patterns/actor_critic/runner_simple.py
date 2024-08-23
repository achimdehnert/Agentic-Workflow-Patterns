from src.config.logging import logger 
from collections import OrderedDict
from src.patterns.actor_critic.generate.generator import generate_draft
from src.patterns.actor_critic.generate.generator import review_draft


history = OrderedDict()


NUM_CYCLES = 2 



topic = 'perplexity'




def dict_to_markdown(data: dict, indent_level: int = 0) -> str:
    """
    Convert a dictionary to a Markdown formatted string with a given indentation level.
    
    Args:
        data (dict): The dictionary to convert.
        indent_level (int): The current level of indentation for nested dictionaries.
    
    Returns:
        str: A Markdown formatted string representing the dictionary.
    """
    markdown = []
    indent = ' ' * indent_level

    for key, value in data.items():
        if isinstance(value, dict):
            markdown.append(f"{indent}- **{key.capitalize()}**:\n")
            markdown.append(dict_to_markdown(value, indent_level + 2))  # Recursive call for nested dicts
        else:
            markdown.append(f"{indent}- **{key.capitalize()}**: {value}\n")

    return ''.join(markdown)


def history_to_markdown(history: OrderedDict) -> str:
    """
    Convert the history OrderedDict to a Markdown formatted string.
    
    Args:
        history (OrderedDict): The history containing drafts and reviews.
    
    Returns:
        str: A Markdown formatted string representing the history.
    """
    markdown = []
    
    for key, value in history.items():
        markdown.append(f"### {key}\n")
        if isinstance(value, dict):
            markdown.append(f"```\n{dict_to_markdown(value)}\n```")
        else:
            markdown.append(f"```\n{value}\n```")
        markdown.append("\n")  
    
    return ''.join(markdown)


for cycle in range(NUM_CYCLES):
    if cycle == 0:
        initial_draft = generate_draft(topic=topic)
        history["Initial Draft"] = initial_draft
        intial_review = review_draft(initial_draft)
        history["Initial Review"] = intial_review
    else:
        pass

history = history_to_markdown(history)
print(history)




