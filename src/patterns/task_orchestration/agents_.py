import json
import os
import re
from glob import glob
import asyncio
from json import JSONDecodeError
from typing import Dict, Any, Optional
from src.config.logging import logger
from src.patterns.task_orchestration.message import Message
from src.patterns.task_orchestration.agent import Agent
from src.llm.generate import ResponseGenerator


def extract_json_from_response(response_text: str) -> Optional[Dict[str, Any]]:
    """
    Extracts JSON content from a response text using a regular expression.

    Args:
        response_text (str): The text containing JSON wrapped in <JSON>...</JSON> tags.

    Returns:
        Optional[Dict[str, Any]]: Extracted JSON data as a dictionary, or None if extraction fails.
    """
    try:
        json_match = re.search(r'<JSON>(.*?)</JSON>', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1).strip()
            return json.loads(json_str)
        else:
            logger.error("No JSON content found in LLM response.")
            return None
    except JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
        return None


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
                    "title": title,
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


class PreprocessDocsAgent(Agent):
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


class ExtractKeyInfoAgent(Agent):
    async def process(self, message: Message) -> Message:
        """
        Extracts key information from the preprocessed documents using an LLM.

        Args:
            message (Message): The input message containing preprocessed documents.

        Returns:
            Message: The message containing extracted key information.
        """
        logger.info(f"{self.name} extracting key information.")
        input_data = message.content

        try:
            self.validate_input(input_data, './data/patterns/task_orchestration/schemas/preprocessed_docs_schema.json')
        except Exception as e:
            logger.error(f"Validation failed for input documents: {e}")
            raise

        response_generator = ResponseGenerator()
        key_info = {"key_info": []}

        for doc in input_data["preprocessed_docs"]:
            doc_id = doc["id"]
            doc_title = doc["title"]
            doc_content = doc["content"]

            llm_input = (
                f"You are a literary analyst. Given the text of a document, extract the following key information:\n"
                f"- List of main characters (only names).\n"
                f"- Major themes explored in the document.\n"
                f"- Important plot points.\n\n"
                f"Provide the output in valid JSON format with keys 'characters', 'themes', and 'plot_points'. "
                f"Each 'characters' field must be an array of strings (character names only), and not include descriptions. "
                f"Do not include any explanations or additional text.\n"
                f"Wrap the JSON output within <JSON>{{...}}</JSON> tags.\n\n"
                f"Document Title: {doc_title}\n"
                f"Document Text:\n{doc_content}"
            )

            logger.info(f"Extracting key information from document '{doc_title}' with ID '{doc_id}' using LLM.")

            try:
                def blocking_call():
                    return response_generator.generate_response(
                        model_name='gemini-1.5-flash-001',
                        system_instruction='',
                        contents=[llm_input]
                    ).text.strip()

                extraction_result = await asyncio.to_thread(blocking_call)
                logger.debug(f"LLM Response for document '{doc_title}': {extraction_result}")

                extracted_data = extract_json_from_response(extraction_result)
                if not extracted_data:
                    logger.error(f"Failed to extract JSON for document '{doc_title}'.")
                    raise ValueError(f"Invalid JSON extraction for document '{doc_title}'")

                characters = extracted_data.get("characters", [])
                themes = extracted_data.get("themes", [])
                plot_points = extracted_data.get("plot_points", [])

                if not isinstance(characters, list) or not all(isinstance(c, str) for c in characters):
                    logger.error(f"Invalid characters format for document '{doc_title}'.")
                    raise ValueError(f"Invalid characters format for document '{doc_title}'")

                if not isinstance(themes, list) or not all(isinstance(t, str) for t in themes):
                    logger.error(f"Invalid themes format for document '{doc_title}'.")
                    raise ValueError(f"Invalid themes format for document '{doc_title}'")

                if not isinstance(plot_points, list) or not all(isinstance(p, str) for p in plot_points):
                    logger.error(f"Invalid plot points format for document '{doc_title}'.")
                    raise ValueError(f"Invalid plot points format for document '{doc_title}'")

                key_info["key_info"].append({
                    "doc_id": doc_id,
                    "characters": characters,
                    "themes": themes,
                    "plot_points": plot_points
                })

            except Exception as e:
                logger.error(f"Failed to extract key information from document '{doc_title}' with ID '{doc_id}': {e}")
                raise RuntimeError(f"Error extracting key information for document '{doc_title}'") from e

        try:
            self.validate_output(key_info, './data/patterns/task_orchestration/schemas/key_info_schema.json')
        except Exception as e:
            logger.error(f"Validation failed for extracted key information: {e}")
            raise

        return Message(content=key_info, sender=self.name, recipient=message.sender)


class GenerateSummariesAgent(Agent):
    async def process(self, message: Message) -> Message:
        """
        Generates summaries of the preprocessed documents using an LLM.

        Args:
            message (Message): The input message containing preprocessed documents.

        Returns:
            Message: The message containing generated summaries.
        """
        logger.info(f"{self.name} generating summaries.")
        input_data = message.content

        try:
            self.validate_input(input_data, './data/patterns/task_orchestration/schemas/preprocessed_docs_schema.json')
        except Exception as e:
            logger.error(f"Validation failed for input documents: {e}")
            raise

        response_generator = ResponseGenerator()
        summaries = {"summaries": []}

        for doc in input_data["preprocessed_docs"]:
            doc_id = doc["id"]
            doc_title = doc["title"]
            doc_content = doc["content"]

            llm_input = (
                f"You are a professional document summarizer. Given the text of a document, provide a concise summary "
                f"that captures the main plot, characters, and themes. The summary should be around 200 words.\n\n"
                f"Provide the summary in valid JSON format with the key 'summary'. "
                f"Do not include any explanations or additional text.\n"
                f"Wrap the JSON output within <JSON>{{...}}</JSON> tags.\n\n"
                f"Document Title: {doc_title}\n"
                f"Document Text:\n{doc_content}"
            )

            logger.info(f"Generating summary for document '{doc_title}' with ID '{doc_id}' using LLM.")

            try:
                def blocking_call():
                    return response_generator.generate_response(
                        model_name='gemini-1.5-flash-001',
                        system_instruction='',
                        contents=[llm_input]
                    ).text.strip()

                summary_result = await asyncio.to_thread(blocking_call)
                logger.debug(f"LLM Response for document '{doc_title}': {summary_result}")

                extracted_data = extract_json_from_response(summary_result)
                if not extracted_data or 'summary' not in extracted_data:
                    logger.error(f"Failed to extract summary for document '{doc_title}'.")
                    raise ValueError(f"Invalid summary extraction for document '{doc_title}'")

                summaries["summaries"].append({
                    "doc_id": doc_id,
                    "summary": extracted_data['summary']
                })

            except Exception as e:
                logger.error(f"Failed to generate summary for document '{doc_title}' with ID '{doc_id}': {e}")
                raise RuntimeError(f"Error generating summary for document '{doc_title}'") from e

        try:
            self.validate_output(summaries, './data/patterns/task_orchestration/schemas/summaries_schema.json')
        except Exception as e:
            logger.error(f"Validation failed for generated summaries: {e}")
            raise

        return Message(content=summaries, sender=self.name, recipient=message.sender)


class CompileReportAgent(Agent):
    async def process(self, message: Message) -> Message:
        """
        Compiles a final report based on key information and summaries.

        Args:
            message (Message): The input message containing key information and summaries.

        Returns:
            Message: The message containing the compiled report.
        """
        logger.info(f"{self.name} compiling final report.")
        input_data = message.content

        try:
            self.validate_input(input_data['task3'], './data/patterns/task_orchestration/schemas/key_info_schema.json')
            self.validate_input(input_data['task4'], './data/patterns/task_orchestration/schemas/summaries_schema.json')
        except Exception as e:
            logger.error(f"Validation failed for inputs to compile report: {e}")
            raise

        key_info_data = input_data['task3']
        summaries_data = input_data['task4']
        response_generator = ResponseGenerator()
        report_sections = []

        for key_info_entry in key_info_data["key_info"]:
            doc_id = key_info_entry["doc_id"]

            summary_entry = next(
                (s for s in summaries_data["summaries"] if s["doc_id"] == doc_id), None)

            if not summary_entry:
                logger.warning(f"No summary found for document ID '{doc_id}'. Skipping.")
                continue

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
                        model_name='gemini-1.5-flash-001',
                        system_instruction='',
                        contents=[llm_input]
                    ).text.strip()

                report_section = await asyncio.to_thread(blocking_call)
                report_sections.append(report_section)

            except Exception as e:
                logger.error(f"Failed to compile report section for document ID '{doc_id}': {e}")
                raise RuntimeError(f"Error compiling report section for document '{doc_id}'") from e

        report = {"report": "\n\n".join(report_sections)}

        try:
            self.validate_output(report, './data/patterns/task_orchestration/schemas/final_report_schema.json')
        except Exception as e:
            logger.error(f"Validation failed for compiled report: {e}")
            raise

        return Message(content=report, sender=self.name, recipient=message.sender)
