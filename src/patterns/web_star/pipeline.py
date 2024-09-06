from src.patterns.web_star.factory import TaskFactory
from src.patterns.web_star.tasks import SummarizeTask
from src.patterns.web_star.observers import Observer
from src.patterns.web_star.tasks import SearchTask
from src.patterns.web_star.tasks import ScrapeTask
from src.config.logging import logger
from dataclasses import dataclass
from functools import lru_cache 
from dataclasses import field 
from typing import List


@dataclass
class Pipeline:
    search_task: SearchTask
    scrape_task: ScrapeTask
    summarize_task: SummarizeTask
    observers: List[Observer] = field(default_factory=list)

    def add_observer(self, observer: Observer):
        self.observers.append(observer)

    def notify_observers(self, message: str):
        for observer in self.observers:
            observer.update(message)

    def run(self, model_name: str, query: str) -> None:
        try:
            self.notify_observers("Pipeline execution started")
            
            self.notify_observers("Executing web search...")
            self.search_strategy.execute(model_name, query)
            
            self.notify_observers("Starting web scraping...")
            self.scraping_strategy.run()
            
            self.notify_observers("Summarizing scraped content...")
            self.summarization_strategy.summarize(model_name, query)
            
            self.notify_observers("Pipeline execution completed")
        except Exception as e:
            logger.error(f"An error occurred during the pipeline execution: {e}", exc_info=True)
            raise
