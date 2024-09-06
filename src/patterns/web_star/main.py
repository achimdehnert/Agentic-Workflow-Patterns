from functools import lru_cache 
from src.patterns.web_star.factory import TaskFactory
from src.patterns.web_star.tasks import SearchTask
from src.patterns.web_star.tasks import ScrapeTask
from src.patterns.web_star.tasks import SummarizeTask
from src.patterns.web_star.pipeline import Pipeline
from src.patterns.web_star.observers import LogObserver
from src.patterns.web_star.observers import ProgressObserver


class Container:
    @lru_cache()
    def search_strategy(self) -> SearchTask:
        return TaskFactory.create_search_task()

    @lru_cache()
    def scraping_strategy(self) -> ScrapeTask:
        return TaskFactory.create_scrape_task()

    @lru_cache()
    def summarization_strategy(self) -> SummarizeTask:
        return TaskFactory.create_summarize_task()

    @lru_cache()
    def pipeline(self) -> Pipeline:
        pipeline = Pipeline(
            self.search_strategy(),
            self.scraping_strategy(),
            self.summarization_strategy()
        )
        pipeline.add_observer(LogObserver())
        pipeline.add_observer(ProgressObserver())
        return pipeline
    

if __name__ == '__main__':
    container = Container()
    pipeline = container.pipeline()
    query = 'best hotels in Key West, Florida'
    pipeline.run('gemini-1.5-pro-001', query)