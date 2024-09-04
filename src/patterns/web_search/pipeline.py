from src.patterns.web_search.summarize import WebContentSummarizer
from src.patterns.web_search.search import WebSearchExecutor
from src.patterns.web_search.scrape import WebScraper
from src.config.logging import logger


class Pipeline:
    """
    Pipeline class orchestrates the process of executing a web search, scraping the web pages,
    and summarizing the content. It integrates the components of search, scraping, and summarization.
    """

    def __init__(self) -> None:
        """
        Initializes the pipeline by instantiating the WebSearchExecutor, WebScraper, and WebContentSummarizer.
        """
        self.web_search_executor = WebSearchExecutor()
        self.web_scraper = WebScraper()
        self.web_content_summarizer = WebContentSummarizer()

    def run(self, query: str) -> str:
        """
        Runs the pipeline to search, scrape, and summarize web content for a given query.

        :param query: The search query as a string
        :return: The summarized content as a string
        :raises: Any exception encountered during search, scraping, or summarization.
        """
        try:
            logger.info(f"Starting pipeline for query: {query}")

            # Step 1: Execute web search
            logger.info("Executing web search...")
            search_results = self.web_search_executor.search(query)
            logger.info(f"Search completed with {len(search_results)} results.")

            # Step 2: Scrape web pages
            logger.info("Starting web scraping...")
            scraped_data = self.web_scraper.scrape(search_results)
            logger.info(f"Scraping completed with {len(scraped_data)} pages scraped.")

            # Step 3: Summarize content
            logger.info("Summarizing content...")
            summary = self.web_content_summarizer.summarize(scraped_data)
            logger.info("Content summarization completed.")

            return summary

        except Exception as e:
            logger.error(f"An error occurred during the pipeline execution: {e}", exc_info=True)
            raise


if __name__ == '__main__':
    query = 'best hotels in Key West, Florida'
    pipeline = Pipeline()
    pipeline.run(query)
