from src.patterns.web_search.summarize import WebContentSummarizer
from src.patterns.web_search.search import WebSearchExecutor
from src.patterns.web_search.scrape import WebScraper
from src.config.logging import logger 


class Pipeline:
    def __init__(self):
        self.web_search_executor = WebSearchExecutor()
        self.web_scraper = WebScraper()
        self.web_content_summarizer = WebContentSummarizer()
    
    def run(self, query) -> str:
        self.web_search_executor.search()

        # step 2
        self.web_scraper.scrape()

        # step 3
        self.web_content_summarizer.summarize()
        



if __name__ == '__main__':
    query = 'best hotels in keywest florida'
    pipeline = Pipeline()
    pipeline.run(query)





