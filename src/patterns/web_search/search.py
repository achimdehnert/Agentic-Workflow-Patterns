from vertexai.preview.generative_models import FunctionDeclaration
from vertexai.preview.generative_models import GenerationResponse
from vertexai.preview.generative_models import Tool
from src.llm.generate import ResponseGenerator
from src.prompt.manage import TemplateManager
from src.patterns.web_search.serp import run
from src.config.logging import logger
from typing import Optional
from typing import Dict 
from typing import Any 


class WebSearchExecutor:
    """
    A class to manage the creation and execution of web search queries using Vertex AI generative models.
    
    Attributes:
        response_generator (ResponseGenerator): The generator for creating model responses.
        template_manager (TemplateManager): The manager for handling prompt templates.
    """
    
    TEMPLATE_PATH = './config/patterns/web_search.yml'

    def __init__(self):
        """
        Initializes the WebSearchExecutor with the static template configuration.
        """
        self.response_generator = ResponseGenerator()
        self.template_manager = TemplateManager(self.TEMPLATE_PATH)
    
    def create_search_function_declaration(self) -> FunctionDeclaration:
        """
        Creates a function declaration for performing a web search with an optional location parameter.
        
        Returns:
            FunctionDeclaration: A declaration specifying the structure of the search function.
        """
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

    def function_call(self, search_query: str, search_tool: Tool) -> GenerationResponse:
        """
        Executes the function call using Gemini to derive the arguments for the API call.

        Args:
            search_query (str): The search query used for web search.
            search_tool (Tool): Configuration for generating search data.

        Returns:
            GenerationResponse: The response from the model with the generated content.

        Raises:
            Exception: If there is an issue with generating the content.
        """
        try:
            # Create a template for the search tool interaction
            template = self.template_manager.create_template('tools', 'search')
            system_instruction = template['system']
            
            # Fill the user template with the provided search query
            user_instruction = self.template_manager.fill_template(template['user'], query=search_query)
            
            # Generate and return the response using the system and user instructions
            return self.response_generator.generate_response(system_instruction, [user_instruction], tools=[search_tool])
        
        except Exception as e:
            # Log error and raise exception if content generation fails
            logger.error(f"Error generating search data: {e}")
            raise

    def extract_function_args(self, response: GenerationResponse) -> Optional[Dict[str, Any]]:
        """
        Extracts arguments from the first function call in the first candidate of the response.
        
        Args:
            response (GenerationResponse): The response containing generated content.
        
        Returns:
            Optional[Dict[str, Any]]: The extracted arguments if present, otherwise None.
        """
        try:
            first_candidate = response.candidates[0]
            first_part = first_candidate.content.parts[0]
            function_call = first_part.function_call
            
            if function_call:
                return dict(function_call.args)
            else:
                logger.info("No function call found in the first part of the first candidate.")
                return None
        except (IndexError, KeyError) as e:
            logger.error(f"Failed to extract function arguments: {e}")
            return None

    def execute(self, query: str) -> None:
        """
        Simplified search execution method. Calls the web search function with just the query.
        
        Args:
            query (str): The query to search for.
        """
        search_tool = Tool(function_declarations=[self.create_search_function_declaration()])
        response = self.function_call(query, search_tool)
        function_args = self.extract_function_args(response)
        
        if function_args:
            search_query = function_args.get('query', query)  # fallback to original query if not in args
            location = function_args.get('location', '')
            run(search_query, location)


if __name__ == "__main__":
    search_executor = WebSearchExecutor()
    search_executor.execute("greek restaurants in frisco")
