
from src.patterns.task_orchestration.message import Message
from src.patterns.task_orchestration.agent import Agent
from src.config.logging import logger 
import asyncio


class GenerateSummariesAgent(Agent):
    async def process(self, message: Message) -> Message:
        logger.info(f"{self.name} generating summaries.")
        input_data = message.content
        self.validate_input(input_data, 'preprocessed_books_schema.json')
        await asyncio.sleep(1)
        # Simulate summary generation
        summaries = {
            "summaries": [
                {
                    "book_id": book["id"],
                    "summary": f"Summary of {book['title']}: {book['content'][:100]}..."
                }
                for book in input_data["preprocessed_books"]
            ]
        }
        self.validate_output(summaries, 'summaries_schema.json')
        return Message(content=summaries, sender=self.name, recipient=message.sender)
