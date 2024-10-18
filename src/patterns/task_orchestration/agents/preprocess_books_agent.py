from src.patterns.task_orchestration.message import Message
from src.patterns.task_orchestration.agent import Agent
from src.config.logging import logger 
import asyncio

class PreprocessBooksAgent(Agent):
    async def process(self, message: Message) -> Message:
        logger.info(f"{self.name} preprocessing books.")
        input_data = message.content
        # Validate input against schema
        self.validate_input(input_data, 'book_collection_schema.json')
        await asyncio.sleep(1)
        # Simulate preprocessing
        preprocessed_books = {
            "preprocessed_books": [
                {
                    "id": book["id"],
                    "title": book["title"],
                    "content": book["content"].lower()  # Simple preprocessing
                }
                for book in input_data["books"]
            ]
        }
        self.validate_output(preprocessed_books, 'preprocessed_books_schema.json')
        return Message(content=preprocessed_books, sender=self.name, recipient=message.sender)
