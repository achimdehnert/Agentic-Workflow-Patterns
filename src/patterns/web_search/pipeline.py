from src.patterns.web_search.tasks import SummarizeTask
from src.patterns.web_search.tasks import SearchTask
from src.patterns.web_search.tasks import ScrapeTask
from src.config.logging import logger
from dataclasses import dataclass

@dataclass
class Pipeline:
    """
    Pipeline class that orchestrates the execution of search, scrape, and summarize tasks.
    
    Attributes:
        search_task (SearchTask): The task responsible for searching web content.
        scrape_task (ScrapeTask): The task responsible for scraping web content.
        summarize_task (SummarizeTask): The task responsible for summarizing the scraped content.
    """
    search_task: SearchTask
    scrape_task: ScrapeTask
    summarize_task: SummarizeTask

    def run(self, model_name: str, query: str) -> None:
        """
        Executes the search, scrape, and summarize tasks in sequence.
        
        Args:
            model_name (str): The model name used for the summarization task.
            query (str): The search query that will be passed to the search and summarize tasks.
        
        Raises:
            Exception: If any task encounters an error, the exception is logged and re-raised.
        """
        try:
            logger.info(f"Starting pipeline execution for query: '{query}' with model: '{model_name}'.")
            
            # Execute the search task
            logger.info("Executing search task.")
            self.search_task.run(model_name, query)
            
            # Execute the scrape task
            logger.info("Executing scrape task.")
            self.scrape_task.run()

            # Execute the summarize task
            logger.info("Executing summarize task.")
            self.summarize_task.run(model_name, query)
            
            logger.info("Pipeline execution completed successfully.")
        
        except Exception as e:
            logger.error(f"An error occurred during the pipeline execution: {e}", exc_info=True)
            raise
