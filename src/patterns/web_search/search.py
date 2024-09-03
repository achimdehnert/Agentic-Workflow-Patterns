from vertexai.preview.generative_models import FunctionDeclaration
from vertexai.preview.generative_models import GenerationResponse
from vertexai.preview.generative_models import Tool
from src.patterns.web_search.search import run
from src.llm.generate import ResponseGenerator
from src.prompt.manage import TemplateManager
from src.config.logging import logger
from typing import Optional, Dict, Any


response_generator = ResponseGenerator()
template_manager = TemplateManager('./config/patterns/web_search.yml')


def create_search_function_declaration() -> FunctionDeclaration:
    """
    Creates a function declaration for performing a web search with optional location parameter.
    
    Returns:
        FunctionDeclaration: A declaration that specifies the structure of the search function.
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


def perform_search(search_query: str, search_tool: Tool) -> GenerationResponse:
    """
    Generates a search result based on a provided search query and tool specifications.
    
    Args:
        search_query (str): The query to be used for the web search.
        search_tool (Tool): The tool configuration for generating search data.
    
    Returns:
        GenerationResponse: The response from the model containing generated content.
    
    Raises:
        Exception: If there's an issue generating the content.
    """
    try:
        template = template_manager.create_template('tools', 'search')
        system_instruction = template['system']
        user_instruction = template_manager.fill_template(template['user'], query=search_query)
      
        return response_generator.generate_response(system_instruction, [user_instruction], tools=[search_tool])
    except Exception as e:
        logger.error(f"Failed to generate search data: {e}")
        raise


def extract_function_args(response: GenerationResponse) -> Optional[Dict[str, Any]]:
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


def run_search(args: Dict[str, Any]) -> None:
    """
    Runs the search using the extracted arguments, ensuring that the query and location parameters are passed correctly.

    Args:
        args (Dict[str, Any]): The arguments to be passed to the search function, including `query` and `location`.
    """
    query = args.get('query')
    location = args.get('location')

    # Pass query and location as separate arguments to the run function
    run(query, location)



if __name__ == "__main__":
    prompt = "greek restaurants in frisco"  
    search_tool = Tool(function_declarations=[create_search_function_declaration()])
    logger.info(search_tool)
    response = perform_search(prompt, search_tool)
    function_args = extract_function_args(response)
    logger.info(function_args)
    if function_args:
        run_search(function_args)

