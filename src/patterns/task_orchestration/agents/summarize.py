from src.patterns.task_orchestration.agents.commons import extract_json_from_response
from src.patterns.task_orchestration.message import Message
from src.patterns.task_orchestration.agent import Agent
from src.llm.generate import ResponseGenerator
from src.config.logging import logger
import asyncio
import os


class SummarizeAgent(Agent):
    ROOT_PATTERN_PATH = './data/patterns/task_orchestration'
    INPUT_SCHEMA_PATH = os.path.join(ROOT_PATTERN_PATH, 'schemas', 'preprocessed_docs_schema.json')
    OUTPUT_SCHEMA_PATH = os.path.join(ROOT_PATTERN_PATH, 'schemas', 'summaries_schema.json')
    MODEL_NAME = 'gemini-1.5-flash-001'

    async def process(self, message: Message) -> Message:
        """
        Generates summaries of the preprocessed documents using an LLM.

        Args:
            message (Message): The input message containing preprocessed documents.

        Returns:
            Message: The message containing generated summaries.

        Raises:
            RuntimeError: If document summarization or validation fails.
        """
        logger.info(f"{self.name} started generating summaries.")
        input_data = message.content

        # Validate the input data against the defined schema
        self._validate_input_data(input_data)

        response_generator = ResponseGenerator()
        summaries = {"summaries": []}

        for doc in input_data.get("preprocessed_docs", []):
            try:
                summary = await self._generate_summary(
                    response_generator, doc["id"], doc["title"], doc["content"]
                )

                summaries["summaries"].append({
                    "doc_id": doc["id"],
                    "summary": summary
                })
            except Exception as e:
                logger.error(f"Failed to generate summary for document '{doc['title']}' with ID '{doc['id']}': {e}")
                raise RuntimeError(f"Error generating summary for document '{doc['title']}'") from e

        # Validate the generated summaries against the output schema
        self._validate_output_data(summaries)

        logger.info(f"{self.name} successfully generated and validated summaries.")
        return Message(content=summaries, sender=self.name, recipient=message.sender)

    async def _generate_summary(self, response_generator: ResponseGenerator, doc_id: str, doc_title: str, doc_content: str) -> str:
        """
        Generates a summary for a document using an LLM.

        Args:
            response_generator (ResponseGenerator): The LLM response generator instance.
            doc_id (str): The ID of the document being processed.
            doc_title (str): The title of the document.
            doc_content (str): The content of the document.

        Returns:
            str: The generated summary in JSON format.

        Raises:
            RuntimeError: If the LLM fails to generate a response.
        """
        llm_input = (
            "You are a professional document summarizer. Given the text of a document, provide a concise summary "
            "that captures the main plot, characters, and themes. The summary should be short and limited to only two sentences.\n\n"
            "Provide the summary in valid JSON format with the key 'summary'. "
            "Do not include any explanations or additional text.\n"
            "Wrap the JSON output within <JSON>{{...}}</JSON> tags.\n\n"
            f"Document Title: {doc_title}\n"
            f"Document Text:\n{doc_content}"    
        )
        logger.info(f"Generating summary for document '{doc_title}' with ID '{doc_id}' using LLM.")

        try:
            def blocking_call():
                return response_generator.generate_response(
                    model_name=self.MODEL_NAME,
                    system_instruction='',
                    contents=[llm_input]
                ).text.strip()

            summary_result = await asyncio.to_thread(blocking_call)
            logger.debug(f"LLM Response for document '{doc_title}': {summary_result}")

            extracted_data = extract_json_from_response(summary_result)
            if not extracted_data or 'summary' not in extracted_data:
                logger.error(f"Failed to extract summary for document '{doc_title}'.")
                raise ValueError(f"Invalid summary extraction for document '{doc_title}'")

            return extracted_data['summary']
        except Exception as e:
            logger.error(f"Failed to generate summary for document '{doc_title}' with ID '{doc_id}': {e}")
            raise RuntimeError(f"Error generating summary for document '{doc_title}'") from e

    def _validate_input_data(self, input_data: dict) -> None:
        """
        Validates the input data using the defined input schema.

        Args:
            input_data (dict): The input data to validate.

        Raises:
            RuntimeError: If input validation fails.
        """
        try:
            self.validate_input(input_data, self.INPUT_SCHEMA_PATH)
        except Exception as e:
            logger.error(f"Validation failed for input documents: {e}")
            raise RuntimeError(f"Validation failed for input documents") from e

    def _validate_output_data(self, output_data: dict) -> None:
        """
        Validates the output data using the defined output schema.

        Args:
            output_data (dict): The output data to validate.

        Raises:
            RuntimeError: If output validation fails.
        """
        try:
            self.validate_output(output_data, self.OUTPUT_SCHEMA_PATH)
        except Exception as e:
            logger.error(f"Validation failed for generated summaries: {e}")
            raise RuntimeError(f"Validation failed for generated summaries") from e
