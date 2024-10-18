from src.patterns.task_orchestration.message import Message
from src.patterns.task_orchestration.agent import Agent
from src.config.logging import logger 
from glob import glob
import os 


class CollectBooksAgent(Agent):
    async def process(self, message: Message) -> Message:
        logger.info(f"{self.name} collecting books.")
        folder_path = './data/patterns/task_orchestration/books'  # Folder containing book text files
        book_files = glob(os.path.join(folder_path, '*.txt'))
        books = {
            "books": []
        }
        for idx, filepath in enumerate(book_files):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            title = os.path.splitext(os.path.basename(filepath))[0]
            books["books"].append({
                "id": f"book{idx+1}",
                "title": title,
                "content": content,
                "filename": filepath
            })
        # Validate output against schema
        self.validate_output(books, 'book_collection_schema.json')
        return Message(content=books, sender=self.name, recipient=message.sender)
