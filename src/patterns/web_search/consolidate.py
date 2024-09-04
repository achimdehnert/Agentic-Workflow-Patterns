from src.patterns.web_search.scrape import WebScraper
from src.llm.generate import ResponseGenerator
from src.config.logging import logger 

from src.prompt.manage import TemplateManager
from src.utils.io import read_file


query = 'best hotels in key west florida'

input_data_path = './data/patterns/web_search/output/scrape/scraped_content.txt'
html_content = read_file(input_data_path)
template_manager = TemplateManager('./config/patterns/web_search.yml')
template = template_manager.create_template('tools', 'scrape')
system_instruction = template['system']

user_instruction = template_manager.fill_template(template['user'], query=query, html_content=html_content)
response_generator = ResponseGenerator()    
response = response_generator.generate_response(system_instruction, [user_instruction])
print(response)
        