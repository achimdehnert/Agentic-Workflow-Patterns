import logging
from writer.writer import Writer
from evaluator.evaluator import Evaluator

class Router:
    def __init__(self, writer: Writer, evaluator: Evaluator) -> None:
        """
        Initializes the Router with a Writer and an Evaluator.

        :param writer: An instance of Writer to generate content.
        :param evaluator: An instance of Evaluator to critique the content.
        """
        self.writer = writer
        self.evaluator = evaluator

    def route(self, input_data: str, cycle: int) -> (str, str):
        """
        Routes the data through the Writer and Evaluator, depending on the current cycle.

        :param input_data: The data to be processed.
        :param cycle: The current cycle number.
        :return: A tuple of the processed data and its status.
        """
        try:
            if cycle == 0:
                processed_data = self.writer.process(input_data, "blog")
            else:
                processed_data = self.writer.process(input_data, "revise")
            evaluation_status = self.evaluator.evaluate(processed_data, input_data)
            return processed_data, evaluation_status
        except Exception as e:
            logging.error(f"Error in routing: {e}")
            return "", "error"
