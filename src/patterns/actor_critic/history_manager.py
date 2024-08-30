from src.config.logging import logger
from collections import OrderedDict
from typing import Dict
from typing import Any 


class HistoryManager:
    def __init__(self):
        self.history = OrderedDict()
        self.history_md = None

    def add_entry(self, key: str, value: Any) -> None:
        try:
            self.history[key] = value
            self.history_md = self.to_markdown()
        except Exception as e:
            logger.error(f"Error adding entry to history: {e}")
            raise

    def to_markdown(self) -> str:
        try:
            markdown = []
            for key, value in self.history.items():
                markdown.append(f"### {key}\n")
                if isinstance(value, dict):
                    markdown.append(f"\n{self.dict_to_markdown(value)}\n")
                else:
                    markdown.append(f"\n{value}\n")
                markdown.append("\n")  
            return ''.join(markdown)
        except Exception as e:
            logger.error(f"Error converting history to markdown: {e}")
            raise

    @staticmethod
    def dict_to_markdown(data: Dict[str, Any], indent_level: int = 0) -> str:
        try:
            markdown = []
            indent = ' ' * indent_level
            for key, value in data.items():
                if isinstance(value, dict):
                    markdown.append(f"{indent}- **{key.capitalize()}**:\n")
                    markdown.append(HistoryManager.dict_to_markdown(value, indent_level + 2))
                else:
                    markdown.append(f"{indent}- **{key.capitalize()}**: {value}\n")
            return ''.join(markdown)
        except Exception as e:
            logger.error(f"Error converting dictionary to markdown: {e}")
            raise

    def get_history(self) -> OrderedDict:
        return self.history