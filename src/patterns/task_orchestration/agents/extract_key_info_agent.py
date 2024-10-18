from src.patterns.task_orchestration.message import Message
from src.patterns.task_orchestration.agent import Agent
from src.config.logging import logger 
import asyncio


class ExtractKeyInfoAgent(Agent):
    async def process(self, message: Message) -> Message:
        logger.info(f"{self.name} extracting key information.")
        input_data = message.content
        self.validate_input(input_data, 'preprocessed_books_schema.json')
        await asyncio.sleep(1)
        # Simulate key information extraction
        key_info = {
            "key_info": [
                {
                    "book_id": book["id"],
                    "characters": ["character1", "character2"],  # Dummy data
                    "themes": ["theme1", "theme2"],
                    "plot_points": ["plot point1", "plot point2"]
                }
                for book in input_data["preprocessed_books"]
            ]
        }
        self.validate_output(key_info, 'key_info_schema.json')
        return Message(content=key_info, sender=self.name, recipient=message.sender)
