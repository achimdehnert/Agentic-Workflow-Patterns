from collections import OrderedDict
from typing import Dict 
from typing import Any 


class HistoryManager:
    """
    Manages the history of drafts and reviews, and provides functionality to convert it into Markdown format.
    """
    
    def __init__(self):
        self.history = OrderedDict()
        self.history_md = None

    def add_entry(self, key: str, value: Any) -> None:
        """
        Add an entry to the history.
        
        Args:
            key (str): The key for the history entry.
            value (Any): The value for the history entry.
        """
        self.history[key] = value
        self.history_md = self.to_markdown()

    def to_markdown(self) -> str:
        """
        Convert the history to a Markdown formatted string.
        
        Returns:
            str: A Markdown formatted string representing the history.
        """
        markdown = []

        for key, value in self.history.items():
            markdown.append(f"### {key}\n")
            if isinstance(value, dict):
                markdown.append(f"\n{self.dict_to_markdown(value)}\n")
            else:
                markdown.append(f"\n{value}\n")
            markdown.append("\n")  

        return ''.join(markdown)

    @staticmethod
    def dict_to_markdown(data: Dict[str, Any], indent_level: int = 0) -> str:
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
                markdown.append(HistoryManager.dict_to_markdown(value, indent_level + 2))  # Recursive call for nested dicts
            else:
                markdown.append(f"{indent}- **{key.capitalize()}**: {value}\n")

        return ''.join(markdown)

    def get_history(self) -> OrderedDict:
        """
        Get the current history.
        
        Returns:
            OrderedDict: The history containing drafts and reviews.
        """
        return self.history