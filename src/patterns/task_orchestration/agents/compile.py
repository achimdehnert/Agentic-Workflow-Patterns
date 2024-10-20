from src.patterns.task_orchestration.message import Message
from src.patterns.task_orchestration.agent import Agent
from src.llm.generate import ResponseGenerator
from src.config.logging import logger
import asyncio
import os


class CompileAgent(Agent):
    ROOT_PATTERN_PATH = './data/patterns/task_orchestration'
    KEY_INFO_SCHEMA_PATH = os.path.join(ROOT_PATTERN_PATH, 'schemas', 'key_info_schema.json')
    SUMMARIES_SCHEMA_PATH = os.path.join(ROOT_PATTERN_PATH, 'schemas', 'summaries_schema.json')
    FINAL_REPORT_SCHEMA_PATH = os.path.join(ROOT_PATTERN_PATH, 'schemas', 'final_report_schema.json')
    MODEL_NAME = 'gemini-1.5-flash-001'

    async def process(self, message: Message) -> Message:
        """
        Compiles a final report based on key information and summaries.

        Args:
            message (Message): The input message containing key information and summaries.

        Returns:
            Message: The message containing the compiled report.

        Raises:
            RuntimeError: If report compilation or validation fails.
        """
        logger.info(f"{self.name} started compiling final report.")
        input_data = message.content

        # Validate the input data for key information and summaries
        self._validate_input_data(input_data)

        key_info_data = input_data['task3']
        summaries_data = input_data['task4']
        response_generator = ResponseGenerator()
        report_sections = []

        for key_info_entry in key_info_data["key_info"]:
            try:
                report_section = await self._compile_report_section(
                    response_generator, key_info_entry, summaries_data
                )
                if report_section:
                    report_sections.append(report_section)
            except Exception as e:
                logger.error(f"Failed to compile report section for document ID '{key_info_entry['doc_id']}': {e}")
                raise RuntimeError(f"Error compiling report section for document '{key_info_entry['doc_id']}'") from e

        report = {"report": "\n\n".join(report_sections)}

        # Validate the compiled report against the final report schema
        self._validate_output_data(report)

        logger.info(f"{self.name} successfully compiled and validated the final report.")
        return Message(content=report, sender=self.name, recipient=message.sender)

    async def _compile_report_section(self, response_generator: ResponseGenerator, key_info_entry: dict, summaries_data: dict) -> str:
        """
        Compiles a report section based on key information and summary using an LLM.

        Args:
            response_generator (ResponseGenerator): The LLM response generator instance.
            key_info_entry (dict): The key information entry for a document.
            summaries_data (dict): The summaries data for all documents.

        Returns:
            str: The compiled report section.

        Raises:
            RuntimeError: If the LLM fails to generate a response.
        """
        doc_id = key_info_entry["doc_id"]
        summary_entry = next(
            (s for s in summaries_data["summaries"] if s["doc_id"] == doc_id), None
        )

        if not summary_entry:
            logger.warning(f"No summary found for document ID '{doc_id}'. Skipping.")
            return None

        llm_input = (
            f"You are a report compiler. Given the summary and key information of a document, "
            f"compile a well-formatted report section for this document. The report should include:\n"
            f"- Title of the document.\n"
            f"- Summary.\n"
            f"- List of main characters with descriptions.\n"
            f"- Major themes.\n"
            f"- Important plot points.\n\n"
            f"Provide the report section in a clear and structured format.\n\n"
            f"Document Title: {summary_entry['doc_id']}\n"
            f"Summary:\n{summary_entry['summary']}\n\n"
            f"Characters:\n{key_info_entry['characters']}\n\n"
            f"Themes:\n{key_info_entry['themes']}\n\n"
            f"Plot Points:\n{key_info_entry['plot_points']}"
        )

        logger.info(f"Compiling report section for document ID '{doc_id}' using LLM.")

        try:
            def blocking_call():
                return response_generator.generate_response(
                    model_name=self.MODEL_NAME,
                    system_instruction='',
                    contents=[llm_input]
                ).text.strip()

            report_section = await asyncio.to_thread(blocking_call)
            return report_section
        except Exception as e:
            logger.error(f"Failed to compile report section for document ID '{doc_id}': {e}")
            raise RuntimeError(f"Error compiling report section for document '{doc_id}'") from e

    def _validate_input_data(self, input_data: dict) -> None:
        """
        Validates the input data for key information and summaries.

        Args:
            input_data (dict): The input data to validate.

        Raises:
            RuntimeError: If input validation fails.
        """
        try:
            self.validate_input(input_data['task3'], self.KEY_INFO_SCHEMA_PATH)
            self.validate_input(input_data['task4'], self.SUMMARIES_SCHEMA_PATH)
        except Exception as e:
            logger.error(f"Validation failed for inputs to compile report: {e}")
            raise RuntimeError(f"Validation failed for inputs to compile report") from e

    def _validate_output_data(self, output_data: dict) -> None:
        """
        Validates the compiled report against the final report schema.

        Args:
            output_data (dict): The compiled report data to validate.

        Raises:
            RuntimeError: If output validation fails.
        """
        try:
            self.validate_output(output_data, self.FINAL_REPORT_SCHEMA_PATH)
        except Exception as e:
            logger.error(f"Validation failed for compiled report: {e}")
            raise RuntimeError(f"Validation failed for compiled report") from e
