from src.patterns.web_search.factory import TaskFactory
from src.config.logging import logger
from typing import Optional
import shutil
import os

class Pipeline:
    """
    Pipeline class that orchestrates the execution of search, scrape, and summarize tasks.
    """
    def __init__(self):
        self._search_task = TaskFactory.create_search_task()
        self._scrape_task = TaskFactory.create_scrape_task()
        self._summarize_task = TaskFactory.create_summarize_task()
        self._output_folders = [
            './data/patterns/web_search/output/search',
            './data/patterns/web_search/output/scrape',
            './data/patterns/web_search/output/summarize'
        ]

    def _flush_output_folders(self):
        """
        Flushes out all files in the output folders before starting the pipeline.
        """
        for folder in self._output_folders:
            try:
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                logger.info(f"Flushed output folder: {folder}")
            except Exception as e:
                logger.error(f"Error flushing folder {folder}: {str(e)}")

    def execute(self, model_name: str, query: str) -> str:
        """
        Executes the search, scrape, and summarize tasks in sequence.

        Args:
            model_name (str): The name of the model used for the summarization task.
            query (str): The search query passed to the search task and used during summarization.

        Returns:
            str: The summary generated after performing the search, scrape, and summarize tasks.

        Raises:
            Exception: If any task encounters an error, the exception is logged and re-raised.
        """
        try:
            logger.info(f"Starting pipeline execution for query: '{query}' with model: '{model_name}'.")

            logger.info("Flushing output folders.")
            self._flush_output_folders()

            logger.info("Executing search task.")
            self._search_task.run(model_name, query)

            logger.info("Executing scrape task.")
            self._scrape_task.run()

            logger.info("Executing summarize task.")
            summary = self._summarize_task.run(model_name, query)

            logger.info("Pipeline execution completed successfully.")
            return summary

        except Exception as e:
            logger.error(f"An error occurred during the pipeline execution: {e}", exc_info=True)
            raise

def run(query: str, model_name: Optional[str] = 'gemini-1.5-pro-001') -> str:
    """
    Main function that initializes the pipeline and executes it.

    Args:
        query (str): The search query to be processed.
        model_name (Optional[str]): The model name used for summarization. Defaults to 'gemini-1.5-flash-001'.

    Returns:
        str: The summary result from the pipeline execution.

    Raises:
        Exception: If any error occurs during pipeline execution, it is logged and re-raised.
    """
    try:
        logger.info(f"Starting pipeline for query: {query} with model: {model_name}")
        pipeline = Pipeline()
        summary = pipeline.execute(model_name, query)
        logger.info("Pipeline run successfully completed.")
        return summary
    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}")
        raise

if __name__ == '__main__':
    query = 'best hotels in houston, texas'
    summary = run(query)
    logger.info(f"Generated Summary: {summary}")