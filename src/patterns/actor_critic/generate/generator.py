from vertexai.generative_models import GenerativeModel
from src.generate.llm import load_and_fill_template
from src.generate.llm import generate_response
from src.generate.llm import load_json
from src.config.logging import logger 
from src.config.setup import config


def generate_draft() -> None:
    """
    Generate and save content using a generative model based on a given topic.

    Raises:
        Exception: If any error occurs during the content generation process, it is logged and re-raised.
    """
    try:
        logger.info("Starting LLM extraction")
        topic = "perplexity"
        system_instruction = load_and_fill_template('./data/patterns/actor_critic/actor/write/system_instructions.txt', topic)
        print(system_instruction)
        user_instruction = load_and_fill_template('./data/patterns/actor_critic/actor/write/user_instructions.txt', topic)
        response_schema = load_json('./data/patterns/actor_critic/actor/write/response_schema.json')
        if response_schema is None:
            raise ValueError("Response schema could not be loaded.")
        
        model = GenerativeModel(config.TEXT_GEN_MODEL_NAME, system_instruction=system_instruction)
        contents = [user_instruction]
        response = generate_response(model, contents, response_schema)
        print(response['article'])
    except Exception as e:
        logger.error(f"Error in LLM extraction: {e}")
        raise

def review_draft() -> None:
    pass

if __name__ == "__main__":
    pass