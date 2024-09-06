from src.patterns.web_star.summarize import WebContentSummarizeAgent
from src.patterns.web_star.search import WebSearchAgent
from src.patterns.web_star.scrape import WebScrapeAgent
from src.patterns.web_star.tasks import SummarizeTask
from src.patterns.web_star.tasks import SearchTask
from src.patterns.web_star.tasks import ScrapeTask


class TaskFactory:
    @staticmethod
    def create_search_task() -> SearchTask:
        return WebSearchAgent()

    @staticmethod
    def create_scrape_task() -> ScrapeTask:
        return WebScrapeAgent()

    @staticmethod
    def create_summarize_task() -> SummarizeTask:
        return WebContentSummarizeAgent()