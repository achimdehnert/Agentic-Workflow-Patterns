from src.patterns.task_orchestration.message import Message
from src.patterns.task_orchestration.agent import Agent
from src.llm.generate import ResponseGenerator
from src.config.logging import logger
from typing import Tuple
from typing import List
from typing import Dict 
from typing import Any 
from glob import glob
import asyncio
import os


class PreprocessAgent(Agent):
    async def process(self, message: Message) -> Message:
        """
        Preprocesses documents by cleaning the content using an LLM.

        Args:
            message (Message): The input message containing collected documents.

        Returns:
            Message: The message containing preprocessed documents.
        """
        logger.info(f"{self.name} preprocessing documents.")
        input_data = message.content

        try:
            self.validate_input(input_data, './data/patterns/task_orchestration/schemas/doc_collection_schema.json')
        except Exception as e:
            logger.error(f"Validation failed for input documents: {e}")
            raise

        response_generator = ResponseGenerator()
        preprocessed_docs = {"preprocessed_docs": []}

        for doc in input_data["docs"]:
            doc_id = doc["id"]
            doc_title = doc["title"]
            doc_content = doc["content"]

            llm_input = (
                f"You are an expert in text processing. Given the raw text of a document, clean the text by removing any "
                f"markup, correcting OCR errors, and normalizing the formatting while preserving the original content. "
                f"Return the cleaned text only.\n\n"
                f"Document Title: {doc_title}\n"
                f"Raw Document Text:\n{doc_content}"
            )

            logger.info(f"Processing document '{doc_title}' with ID '{doc_id}' using LLM.")

            try:
                def blocking_call():
                    return response_generator.generate_response(
                        model_name='gemini-1.5-flash-001',
                        system_instruction='',
                        contents=[llm_input]
                    ).text.strip()

                cleaned_content = await asyncio.to_thread(blocking_call)

                preprocessed_docs["preprocessed_docs"].append({
                    "id": doc_id,
                    "title": doc_title,
                    "content": cleaned_content
                })

            except Exception as e:
                logger.error(f"Failed to preprocess document '{doc_title}' with ID '{doc_id}': {e}")
                raise RuntimeError(f"Error preprocessing document '{doc_title}'") from e

        try:
            self.validate_output(preprocessed_docs, './data/patterns/task_orchestration/schemas/preprocessed_docs_schema.json')
        except Exception as e:
            logger.error(f"Validation failed for preprocessed documents: {e}")
            raise

        return Message(content=preprocessed_docs, sender=self.name, recipient=message.sender)