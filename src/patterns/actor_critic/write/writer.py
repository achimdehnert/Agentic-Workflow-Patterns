from patterns.actor_critic.generator import generate_draft 
from patterns.actor_critic.generator import revise_draft
from src.config.logging import logger 

class Writer:
    def process(self, input_data: str, task: str) -> str:
        """
        Processes the input data using the specified task.

        :param input_data: The input data to be processed.
        :param task: The task to perform (e.g., "blog", "revise").
        :return: The processed data.
        """
        try:
            if task == "draft":
                output_data = generate_draft(f"Create a blog post on: {input_data}")
            elif task == "revise":
                output_data = revise_draft(f"Revise the following blog: {input_data}")
            logger.info(f"Writer ({task}): {output_data}")
            return output_data
        except Exception as e:
            logger.error(f"Error in Writer process: {e}")
            return ""
