
from vertexai.generative_models import HarmBlockThreshold
from vertexai.generative_models import GenerationConfig
from vertexai.generative_models import GenerativeModel
from vertexai.generative_models import HarmCategory
from vertexai.generative_models import Part
from src.config.logging import logger
from src.config.setup import config
from string import Template
from typing import Optional
from typing import List
from typing import Dict 
from typing import Any 
import json 


def create_generation_config(response_schema: Dict[str, Any]) -> GenerationConfig:
    """
    Create a GenerationConfig instance with specified parameters.

    Args:
        response_schema (Dict[str, Any]): The schema defining the expected response format.

    Returns:
        GenerationConfig: A configured instance of GenerationConfig.
    """
    try:
        logger.info("Creating generation configuration")
        generation_config = GenerationConfig(
            temperature=0.0, 
            top_p=0.0, 
            top_k=1, 
            candidate_count=1, 
            max_output_tokens=8192,
            response_mime_type="application/json",
            response_schema=response_schema
        )
        logger.info("Successfully created generation configuration")
        return generation_config
    except Exception as e:
        logger.error(f"Error creating generation configuration: {e}")
        raise

def create_safety_settings() -> Dict[HarmCategory, HarmBlockThreshold]:
    """
    Create safety settings mapping harm categories to block thresholds.

    Returns:
        Dict[HarmCategory, HarmBlockThreshold]: A dictionary mapping harm categories to block thresholds.
    """
    try:
        logger.info("Creating safety settings")
        safety_settings = {
            HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
        }
        logger.info("Successfully created safety settings")
        return safety_settings
    except Exception as e:
        logger.error(f"Error creating safety settings: {e}")
        raise

def generate_response(model: GenerativeModel, contents: List[Part], response_schema: Dict[str, Any]) -> Any:
    """
    Generate content using the provided generative model and return the response.

    Args:
        model (GenerativeModel): The generative model to use.
        contents (List[Part]): The content parts to be processed by the model.
        response_schema (Dict[str, Any]): The schema defining the expected response format.

    Returns:
        Any: The generated response as a parsed JSON object.
    """
    try:
        logger.info("Generating response using the generative model")
        response = model.generate_content(
            contents,
            generation_config=create_generation_config(response_schema),
            safety_settings=create_safety_settings()
        )
        output_json = json.loads(response.text.strip())
        # logger.info(f"Response JSON: {output_json}")
        return output_json
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response: {e}")
        raise
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise



def load_and_fill_template(template_path: str, topic: str) -> str:
    """
    Load a template from a file and replace all occurrences of {} with the topic.

    Args:
        template_path (str): The path to the template file.
        topic (str): The AI concept to insert into the template.

    Returns:
        str: The filled template as a string.
    """
    try:
        with open(template_path, 'r') as file:
            template_content = file.read()
            logger.info(f"Loaded template content: {template_content}")
            
            # Replace all occurrences of '{}' with the topic
            filled_template = template_content.replace("{}", topic)
            
            logger.info(f"Filled template content: {filled_template}")
            return filled_template
    except FileNotFoundError as e:
        logger.error(f"Template file not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading and filling template: {e}")
        raise


def load_json(filename: str) -> Optional[Dict[str, Any]]:
    """
    Load a JSON file and return its contents.

    Args:
        filename (str): The path to the JSON file.

    Returns:
        Optional[Dict[str, Any]]: The parsed JSON object, or None if an error occurs.
    """
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"File '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        logger.error(f"File '{filename}' contains invalid JSON.")
        return None
    except Exception as e:
        logger.error(f"Error loading JSON file: {e}")
        raise

def generate() -> None:
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

if __name__ == "__main__":
    generate()
