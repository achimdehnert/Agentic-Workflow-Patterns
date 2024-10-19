from src.patterns.task_orchestration.message import Message
from src.patterns.task_orchestration.agent import Agent
from src.config.logging import logger
from glob import glob
import os


class CollectDocsAgent(Agent):
    async def process(self, message: Message) -> Message:
        """
        Collects documents from a specified folder, validates the output, and returns a message.

        Args:
            message (Message): The input message.

        Returns:
            Message: The message containing collected documents.
        """
        logger.info(f"{self.name} collecting documents.")
        folder_path = './data/patterns/task_orchestration/docs'
        doc_files = glob(os.path.join(folder_path, '*.txt'))
        docs = {"docs": []}

        for idx, filepath in enumerate(doc_files):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                title = os.path.splitext(os.path.basename(filepath))[0]

                docs["docs"].append({
                    "id": f"doc{idx + 1}",
                    "title": title,  # TODO
                    "content": content,
                    "filename": filepath
                })
            except Exception as e:
                logger.error(f"Failed to collect document from {filepath}: {e}")
                raise RuntimeError(f"Error collecting document from {filepath}") from e

        try:
            self.validate_output(docs, './data/patterns/task_orchestration/schemas/doc_collection_schema.json')
        except Exception as e:
            logger.error(f"Validation failed for collected documents: {e}")
            raise

        return Message(content=docs, sender=self.name, recipient=message.sender)