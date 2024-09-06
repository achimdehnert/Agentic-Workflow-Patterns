from src.patterns.web_star.observers import ProgressObserver
from src.patterns.web_star.observers import LogObserver
from src.patterns.web_star.factory import TaskFactory
from src.patterns.web_star.tasks import SummarizeTask
from src.patterns.web_star.pipeline import Pipeline
from src.patterns.web_star.tasks import SearchTask
from src.patterns.web_star.tasks import ScrapeTask
from functools import lru_cache 


class Container:
    @lru_cache()
    def search_task(self) -> SearchTask:
        return TaskFactory.create_search_task()

    @lru_cache()
    def scrape_task(self) -> ScrapeTask:
        return TaskFactory.create_scrape_task()

    @lru_cache()
    def summarize_task(self) -> SummarizeTask:
        return TaskFactory.create_summarize_task()

    @lru_cache()
    def pipeline(self) -> Pipeline:
        pipeline = Pipeline(
            self.search_task(),
            self.scrape_task(),
            self.summarize_task()
        )
        pipeline.add_observer(LogObserver())
        pipeline.add_observer(ProgressObserver())
        return pipeline
    

if __name__ == '__main__':
    container = Container()
    pipeline = container.pipeline()
    query = 'best hotels in Key West, Florida'
    pipeline.run('gemini-1.5-pro-001', query)