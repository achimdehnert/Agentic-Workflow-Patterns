from src.llm.generate import ResponseGenerator
from src.prompt.manage import TemplateManager
from src.config.logging import logger
from src.utils.io import read_file


class WebSearchManager:
    """
    A class to manage the web scraping and response generation process.
    
    Attributes:
    ----------
    query : str
        The search query for the web scraping process.
    input_data_path : str
        Path to the file containing scraped HTML content.
    template_manager : TemplateManager
        An instance of the TemplateManager to handle templates.
    response_generator : ResponseGenerator
        An instance of the ResponseGenerator to generate responses from LLM.
    
    Methods:
    -------
    generate_response():
        Generates a response based on system instructions and scraped HTML content.
        
    save_response(output_path: str, response_text: str):
        Saves the generated response text to a file.
    """

    def __init__(self, query: str, input_data_path: str, template_path: str) -> None:
        self.query = query
        self.input_data_path = input_data_path
        self.template_manager = TemplateManager(template_path)
        self.response_generator = ResponseGenerator()
        self.html_content = self._read_html_content()

    def _read_html_content(self) -> str:
        """Reads the HTML content from the file."""
        return read_file(self.input_data_path)

    def generate_response(self) -> str:
        """Generates a response based on the system and user instructions."""
        template = self.template_manager.create_template('tools', 'scrape')
        system_instruction = template['system']
        user_instruction = self.template_manager.fill_template(
            template['user'], query=self.query, html_content=self.html_content
        )
        logger.info("Generating response from LLM...")
        response = self.response_generator.generate_response(system_instruction, [user_instruction])
        return response.text.strip()

    def save_response(self, output_path: str, response_text: str) -> None:
        """Saves the generated response text to a file."""
        logger.info(f"Saving response to {output_path}")
        with open(output_path, 'w') as f:
            f.write(response_text)
        logger.info("Response saved successfully.")


if __name__ == "__main__":
    query = 'greek restaurants frisco texas'
    input_data_path = './data/patterns/web_search/output/scrape/scraped_content.txt'
    output_path = './data/patterns/web_search/output/summary.txt'
    template_path = './config/patterns/web_search.yml'

    web_search_manager = WebSearchManager(query, input_data_path, template_path)
    response_text = web_search_manager.generate_response()
    web_search_manager.save_response(output_path, response_text)
    print(response_text)
