from src.llm.generate import ResponseGenerator
from src.prompt.manage import TemplateManager
from src.config.logging import logger
from src.utils.io import read_file
from typing import Dict


class WebContentSummarizer:
    """
    A class to manage the web scraping, response generation, and summary process.
    
    Attributes:
    ----------
    None
    
    Methods:
    -------
    summarize(query: str) -> None:
        Generates a response based on system instructions, user input, and scraped HTML content, 
        and saves the summary to the output path.
    """

    # Static file paths for input/output operations
    INPUT_DATA_PATH: str = './data/patterns/web_search/output/scrape/scraped_content.txt'
    OUTPUT_PATH: str = './data/patterns/web_search/output/summary.txt'
    TEMPLATE_PATH: str = './config/patterns/web_search.yml'

    def __init__(self) -> None:
        """
        Initializes the WebContentSummarizer class with template manager, 
        response generator, and HTML content.
        """
        self.template_manager: TemplateManager = TemplateManager(self.TEMPLATE_PATH)
        self.response_generator: ResponseGenerator = ResponseGenerator()
        self.html_content: str = self._read_html_content()

    def _read_html_content(self) -> str:
        """
        Reads the HTML content from the predefined file path.
        
        Returns:
        -------
        str:
            The scraped HTML content as a string.
        """
        logger.info(f"Reading HTML content from {self.INPUT_DATA_PATH}")
        return read_file(self.INPUT_DATA_PATH)

    def summarize(self, model_name: str, query: str) -> None:
        """
        Generates a summary by integrating system and user instructions with 
        scraped HTML content and saves the generated summary to a file.
        
        This method handles the process of retrieving the template, filling 
        it with the query and HTML content, generating the response using 
        the LLM, and saving the final output to the specified file.
        
        Parameters:
        ----------
        query : str
            The search query for web scraping and content summarization.
        
        Returns:
        -------
        None
        """
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


if __name__ == "__main__":
    model_name = 'gemini-1.5-flash-001'
    query = 'greek restaurants frisco texas'
    
    summarizer = WebContentSummarizer()
    summarizer.summarize(model_name, query)
