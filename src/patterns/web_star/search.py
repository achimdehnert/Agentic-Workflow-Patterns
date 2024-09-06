from vertexai.preview.generative_models import FunctionDeclaration
from vertexai.preview.generative_models import GenerationResponse
from vertexai.preview.generative_models import Tool
from src.patterns.web_star.tasks import SearchTask
from src.llm.generate import ResponseGenerator
from src.prompt.manage import TemplateManager
from src.config.logging import logger
from typing import Optional
from typing import Dict 
from typing import Any 


class WebSearchAgent(SearchTask):
    TEMPLATE_PATH = './config/patterns/web_search.yml'

    def __init__(self):
        self.response_generator = ResponseGenerator()
        self.template_manager = TemplateManager(self.TEMPLATE_PATH)

    def create_search_function_declaration(self) -> FunctionDeclaration:
        return FunctionDeclaration(
            name="web_search",
            description="Perform Google Search using SERP API",
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "location": {"type": "string", "description": "Geographic location for localized search results", "default": ""},
                },
                "required": ["query"]
            },
        )

    def function_call(self, model_name: str, search_query: str, search_tool: Tool) -> GenerationResponse:
        try:
            template = self.template_manager.create_template('tools', 'search')
            system_instruction = template['system']
            user_instruction = self.template_manager.fill_template(template['user'], query=search_query)
            return self.response_generator.generate_response(model_name, system_instruction, [user_instruction], tools=[search_tool])
        except Exception as e:
            logger.error(f"Error generating search data: {e}")
            raise

    def extract_function_args(self, response: GenerationResponse) -> Optional[Dict[str, Any]]:
        try:
            first_candidate = response.candidates[0]
            first_part = first_candidate.content.parts[0]
            function_call = first_part.function_call
            return dict(function_call.args) if function_call else None
        except (IndexError, KeyError) as e:
            logger.error(f"Failed to extract function arguments: {e}")
            return None

    def execute(self, model_name: str, query: str) -> None:
        search_tool = Tool(function_declarations=[self.create_search_function_declaration()])
        response = self.function_call(model_name, query, search_tool)
        function_args = self.extract_function_args(response)
        
        if function_args:
            search_query = function_args.get('query', query)
            location = function_args.get('location', '')
            from src.patterns.web_search.serp import run
            run(search_query, location)