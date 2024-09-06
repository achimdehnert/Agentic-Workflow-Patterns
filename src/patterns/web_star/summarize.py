from src.patterns.web_star.tasks import SummarizeTask
from src.llm.generate import ResponseGenerator
from src.prompt.manage import TemplateManager
from src.config.logging import logger
from src.utils.io import read_file
from typing import Dict


class WebContentSummarizeAgent(SummarizeTask):
    INPUT_DATA_PATH = './data/patterns/web_search/output/scrape/scraped_content.txt'
    OUTPUT_PATH = './data/patterns/web_search/output/summarize/summary.txt'
    TEMPLATE_PATH = './config/patterns/web_search.yml'

    def __init__(self):
        self.template_manager = TemplateManager(self.TEMPLATE_PATH)
        self.response_generator = ResponseGenerator()
        self.html_content = self._read_html_content()

    def _read_html_content(self) -> str:
        logger.info(f"Reading HTML content from {self.INPUT_DATA_PATH}")
        return read_file(self.INPUT_DATA_PATH)

    def run(self, model_name: str, query: str) -> None:
        logger.info("Fetching and processing template for response generation.")
        template: Dict[str, str] = self.template_manager.create_template('tools', 'scrape')
        
        system_instruction: str = template['system']
        user_instruction: str = self.template_manager.fill_template(
            template['user'], query=query, html_content=self.html_content
        )
        
        logger.info("Generating response from LLM...")
        response = self.response_generator.generate_response(model_name, system_instruction, [user_instruction])
        response_text: str = response.text.strip()
        
        logger.info(f"Saving generated response to {self.OUTPUT_PATH}")
        with open(self.OUTPUT_PATH, 'w') as f:
            f.write(response_text)
        
        logger.info("Response saved successfully.")
        print(response_text)