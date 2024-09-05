from src.patterns.web_search.summarize import WebContentSummarizer
from src.patterns.web_search.search import WebSearchExecutor
from src.patterns.web_search.scrape import WebScraper
from src.config.logging import logger


class Pipeline:
    """
    The Pipeline class orchestrates the process of executing a web search, scraping web pages,
    and summarizing the content. It integrates the components of search, scraping, and summarization.
    """

    def __init__(self) -> None:
        """
        Initializes the pipeline by instantiating the WebSearchExecutor, WebScraper, and WebContentSummarizer.
        """
        self.web_search_executor = WebSearchExecutor()
        self.web_scraper = WebScraper()
        self.web_content_summarizer = WebContentSummarizer()

    def run(self, model_name: str, query: str) -> None:
        """
        Executes the full pipeline to search, scrape, and summarize web content for a given query.

        Parameters:
        -----------
        model_name : str
            The name of the model to be used for summarizing the content.
        query : str
            The search query string.

        Raises:
        -------
        Exception: If an error is encountered during search, scraping, or summarization.
        """
        try:
            logger.info(f"Pipeline execution started for query: '{query}'")

            # Step 1: Execute web search
            logger.info("Executing web search...")
            self.web_search_executor.execute(model_name, query)
            logger.info("Step 1: Web search completed")

            # Step 2: Scrape web pages
            logger.info("Starting web scraping...")
            self.web_scraper.run()
            logger.info("Step 2: Web scraping completed")

            # Step 3: Summarize content
            logger.info("Summarizing scraped content...")
            self.web_content_summarizer.summarize(model_name, query)
            logger.info("Step 3: Content summarization completed")

        except Exception as e:
            logger.error(f"An error occurred during the pipeline execution: {e}", exc_info=True)
            raise


if __name__ == '__main__':
    model_name = 'gemini-1.5-flash-001'
    query = 'best hotels in Key West, Florida'
    pipeline = Pipeline()
    pipeline.run(model_name, query)
