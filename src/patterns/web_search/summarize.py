from src.patterns.web_search.tasks import SummarizeTask
from src.llm.generate import ResponseGenerator
from src.prompt.manage import TemplateManager
from src.config.logging import logger
from src.utils.io import read_file, generate_filename
from typing import Dict
import os

class WebContentSummarizeAgent(SummarizeTask):
    """
    WebContentSummarizeAgent is responsible for summarizing scraped web content
    using a language model and predefined templates.
    
    Attributes:
        INPUT_DIR (str): Path to the directory containing scraped content to be summarized.
        OUTPUT_DIR (str): Path to the directory where the generated summary will be saved.
        TEMPLATE_PATH (str): Path to the template configuration file for generating instructions.
    """
    INPUT_DIR = './data/patterns/web_search/output/scrape'
    OUTPUT_DIR = './data/patterns/web_search/output/summarize'
    TEMPLATE_PATH = './config/patterns/web_search.yml'

    def __init__(self) -> None:
        """
        Initializes WebContentSummarizeAgent with a template manager and response generator.
        """
        self.template_manager = TemplateManager(self.TEMPLATE_PATH)
        self.response_generator = ResponseGenerator()

    def _read_scraped_content(self, query: str) -> str:
        """
        Reads the scraped content from the input data path based on the query.

        Args:
            query (str): The query used to generate the filename.

        Returns:
            str: The scraped content as a string.
        """
        try:
            logger.info(f"Reading scraped content for query '{query}'")
            input_file_path = f'{self.INPUT_DIR}/{generate_filename(query)}'
            return read_file(input_file_path)
        except Exception as e:
            logger.error(f"Error reading scraped content: {e}")
            raise

    def _save_summary(self, summary: str, query: str) -> None:
        """
        Saves the generated summary to a text file.

        Args:
            summary (str): The generated summary to be saved.
            query (str): The query used to generate the filename.
        """
        output_path = f"{self.OUTPUT_DIR}/{generate_filename(query)}.txt"
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            logger.info(f"Saving summary to {output_path}")
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(summary)
            logger.info("Summary saved successfully.")
        except Exception as e:
            logger.error(f"Error saving summary: {e}", exc_info=True)
            raise

    def run(self, model_name: str, query: str) -> str:
        """
        Executes the summarization process, generating a summary of the scraped content
        using the provided language model, and saves the summary to a file.

        Args:
            model_name (str): The name of the model to be used for summarization.
            query (str): The query used to contextualize the summary.

        Returns:
            str: The generated summary.
        """
        try:
            # Reading content specific to the query
            scraped_content = self._read_scraped_content(query)

            # Generating the prompt template
            logger.info("Fetching and processing template for response generation.")
            template: Dict[str, str] = self.template_manager.create_template('tools', 'summarize')
            system_instruction = template['system']
            user_instruction = self.template_manager.fill_template(
                template['user'], query=query, scraped_content=scraped_content
            )

            # Generating response
            logger.info("Generating response from LLM.")
            response = self.response_generator.generate_response(
                model_name, system_instruction, [user_instruction]
            )
            summary = response.text.strip()
            logger.info("Response generated successfully.")

            # Saving the summary
            self._save_summary(summary, query)
            
            return summary
        
        except Exception as e:
            logger.error(f"Error during summarization process: {e}", exc_info=True)
            raise
