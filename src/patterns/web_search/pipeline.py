from src.patterns.web_search.search import WebSearchExecutor
from src.patterns.web_search.scrape import WebScraper
from src.config.logging import logger 



class Pipeline:
    def __init__(self, query) -> None:
        self.query = query 
        web_search_executor = WebSearchExecutor()
        web_scraper = WebScraper()
    
    def run(self) -> str:
        pass



if __name__ == '__main__':
    query = 'best hotels in keywest florida'





