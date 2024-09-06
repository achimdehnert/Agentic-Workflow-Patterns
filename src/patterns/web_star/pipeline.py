from src.patterns.web_star.tasks import SummarizeTask
from src.patterns.web_star.tasks import SearchTask
from src.patterns.web_star.tasks import ScrapeTask
from src.config.logging import logger
from dataclasses import dataclass


@dataclass
class Pipeline:
    search_task: SearchTask
    scrape_task: ScrapeTask
    summarize_task: SummarizeTask

    def run(self, model_name: str, query: str) -> None:
        try:
            self.search_task.run(model_name, query)
            self.scrape_task.run()
            self.summarize_task.run(model_name, query)
        except Exception as e:
            logger.error(f"An error occurred during the pipeline execution: {e}", exc_info=True)
            raise
