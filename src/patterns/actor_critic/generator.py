from vertexai.generative_models import GenerativeModel
from src.generate.llm import (
    load_and_fill_template,
    load_and_fill_template2,
    load_and_fill_template3,
    load_template,
    generate_response,
    load_json,
)
from src.config.logging import logger
from src.config.setup import config
import json


def generate_draft(topic: str) -> str:
    """
    Generate content using a generative model based on a given topic.

    Args:
        topic (str): The topic to generate content for.

    Returns:
        str: The generated article.

    Raises:
        Exception: If any error occurs during the content generation process, it is logged and re-raised.
    """
    try:
        logger.info("Starting LLM extraction for topic: %s", topic)
        system_instruction = load_and_fill_template(
            './data/patterns/actor_critic/actor/draft/system_instructions.txt', topic
        )
        user_instruction = load_and_fill_template(
            './data/patterns/actor_critic/actor/draft/user_instructions.txt', topic
        )
        response_schema = load_json('./data/patterns/actor_critic/actor/draft/response_schema.json')

        if response_schema is None:
            raise ValueError("Response schema could not be loaded.")

        model = GenerativeModel(config.TEXT_GEN_MODEL_NAME, system_instruction=system_instruction)
        contents = [user_instruction]
        response = generate_response(model, contents, response_schema)
        article = response['article']
        logger.info("Article generation successful.")
        return article

    except Exception as e:
        logger.error("Error in LLM extraction: %s", e)
        raise


def review_draft(article: str) -> dict:
    """
    Review the generated article using a generative model.

    Args:
        article (str): The article to be reviewed.

    Returns:
        dict: The response containing the review.

    Raises:
        ValueError: If the response schema could not be loaded.
    """
    try:
        logger.info("Starting review process for the generated article.")
        system_instruction = load_template('./data/patterns/actor_critic/critic/review/system_instructions.txt')
        user_instruction = load_and_fill_template2(
            './data/patterns/actor_critic/critic/review/user_instructions.txt', article=article
        )
        response_schema = load_json('./data/patterns/actor_critic/critic/review/response_schema.json')

        if response_schema is None:
            raise ValueError("Response schema could not be loaded.")

        model = GenerativeModel(config.TEXT_GEN_MODEL_NAME, system_instruction=system_instruction)
        contents = [user_instruction]
        response = generate_response(model, contents, response_schema)
        logger.info("Review generation successful.")
        return response

    except Exception as e:
        logger.error("Error in review process: %s", e)
        raise


def revise_draft(history):
    logger.info('start revise for draft')
    system_instruction = load_template('./data/patterns/actor_critic/actor/revise/system_instructions.txt')
    user_instruction = load_and_fill_template3(
        './data/patterns/actor_critic/actor/revise/user_instructions.txt', history=history
    )
    response_schema = load_json('./data/patterns/actor_critic/actor/revise/response_schema.json')
    if response_schema is None:
        raise ValueError("Response schema could not be loaded.")

    model = GenerativeModel(config.TEXT_GEN_MODEL_NAME, system_instruction=system_instruction)
    contents = [user_instruction]
    response = generate_response(model, contents, response_schema)
    logger.info("Revise draft successful.")
    return response





def revise_review(history):
    logger.info('start revise for review')
    system_instruction = load_template('./data/patterns/actor_critic/critic/revise/system_instructions.txt')
    user_instruction = load_and_fill_template3(
        './data/patterns/actor_critic/critic/revise/user_instructions.txt', history=history
    )
    response_schema = load_json('./data/patterns/actor_critic/critic/revise/response_schema.json')
    if response_schema is None:
        raise ValueError("Response schema could not be loaded.")

    model = GenerativeModel(config.TEXT_GEN_MODEL_NAME, system_instruction=system_instruction)
    contents = [user_instruction]
    response = generate_response(model, contents, response_schema)
    logger.info("Revise review successful.")
    return response


if __name__ == "__main__":
    try:
        article = generate_draft('fscore')
        logger.info("Generated Article: %s", article)
        print("Generated Article:")
        print(json.dumps(article, indent=4))
        print('-' * 100)

        review = review_draft(article)
        logger.info("Generated Review: %s", review)
        print("Generated Review:")
        print(json.dumps(review, indent=4))

    except Exception as e:
        logger.error("An error occurred in the main execution: %s", e)
