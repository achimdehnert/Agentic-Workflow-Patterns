

from concurrent.futures import ThreadPoolExecutor, as_completed
from src.patterns.web_search.tasks import ScrapeTask
from src.config.logging import logger
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from typing import Tuple, Dict, List, Any
import requests
import json
import time
import os
import re

class WebScrapeAgent(ScrapeTask):
    """
    WebScrapeAgent is responsible for scraping website content based on search results.
    
    Attributes:
        INPUT_DIR (str): The directory path where the search results (JSON) are stored.
        OUTPUT_DIR (str): The directory path where the scraped content is saved.
        OUTPUT_FILE (str): The filename where the final scraped content is written.
        MAX_WORKERS (int): The maximum number of concurrent workers for scraping.
    """
    INPUT_DIR = "./data/patterns/web_search/output/search"
    OUTPUT_DIR = "./data/patterns/web_search/output/scrape"
    OUTPUT_FILE = "scraped_content.txt"
    MAX_WORKERS = 10

    def __init__(self) -> None:
        self.output_file = os.path.join(self.OUTPUT_DIR, self.OUTPUT_FILE)

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Cleans up the extracted text by removing extra whitespaces and newlines.
        
        Args:
            text (str): The raw text extracted from the webpage.
        
        Returns:
            str: Cleaned text with unnecessary spaces removed.
        """
        return re.sub(r'\s+', ' ', text).strip()

    @staticmethod
    def get_domain(url: str) -> str:
        """
        Extracts the domain from a given URL.
        
        Args:
            url (str): The full URL.
        
        Returns:
            str: The domain name from the URL.
        """
        return urlparse(url).netloc

    def scrape_website(self, url: str) -> str:
        """
        Scrapes the given website URL and extracts relevant content.
        
        Args:
            url (str): The URL to be scraped.
        
        Returns:
            str: Extracted text content from the webpage, or an empty string in case of an error.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            extracted_text = ' '.join([elem.get_text() for elem in text_elements])
            return self.clean_text(extracted_text)
        except requests.RequestException as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return ""

    def scrape_with_delay(self, result: Dict[str, Any], delay: int) -> Tuple[Dict[str, Any], str]:
        """
        Scrapes a website with an added delay to avoid overwhelming the server.

        Args:
            result (Dict[str, Any]): The search result containing the website URL and metadata.
            delay (int): The delay in seconds before scraping.
        
        Returns:
            Tuple[Dict[str, Any], str]: The original result and the scraped content.
        """
        time.sleep(delay)
        content = self.scrape_website(result['Link'])
        return result, content

    def load_latest_json(self) -> List[Dict[str, Any]]:
        """
        Loads the latest JSON file from the input directory containing search results.
        
        Returns:
            List[Dict[str, Any]]: A list of search results (Top Results) from the latest JSON file.
        
        Raises:
            FileNotFoundError: If no JSON files are found in the input directory.
        """
        try:
            json_files = [f for f in os.listdir(self.INPUT_DIR) if f.endswith('.json')]
            if not json_files:
                raise FileNotFoundError("No JSON files found in the input directory.")
            
            latest_file = max(json_files, key=lambda f: os.path.getmtime(os.path.join(self.INPUT_DIR, f)))
            with open(os.path.join(self.INPUT_DIR, latest_file), 'r') as f:
                data = json.load(f)
            
            logger.info(f"Loaded latest search results from: {latest_file}")
            return data['Top Results']
        except Exception as e:
            logger.error(f"Error loading JSON file: {str(e)}")
            raise

    def scrape_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Scrapes the content from the provided search results concurrently using a thread pool.
        
        Args:
            results (List[Dict[str, Any]]): A list of search result dictionaries.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the title, URL, snippet, and scraped content.
        """
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)
        scraped_results = []
        with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
            future_to_result = {
                executor.submit(self.scrape_with_delay, result, i): result
                for i, result in enumerate(results)
            }
            for future in as_completed(future_to_result):
                try:
                    result, content = future.result()
                    if content:
                        scraped_results.append({
                            'title': result['Title'],
                            'url': result['Link'],
                            'snippet': result['Snippet'],
                            'content': content
                        })
                        logger.info(f"Scraped: {result['Title']}")
                    else:
                        logger.info(f"Skipping {result['Title']} due to no content")
                except Exception as e:
                    logger.error(f"Error processing result: {str(e)}")
        return scraped_results

    def save_results(self, scraped_results: List[Dict[str, Any]]) -> None:
        """
        Saves the scraped results to a file.
        
        Args:
            scraped_results (List[Dict[str, Any]]): A list of scraped results to save.
        """
        try:
            with open(self.output_file, 'w', encoding='utf-8') as outfile:
                for result in scraped_results:
                    outfile.write(f"==== BEGIN ENTRY ====\n")
                    outfile.write(f"TITLE: {result['title']}\n")
                    outfile.write(f"URL: {result['url']}\n")
                    outfile.write(f"SNIPPET: {result['snippet']}\n")
                    outfile.write(f"CONTENT:\n{result['content']}\n")
                    outfile.write(f"==== END ENTRY ====\n\n")
            logger.info(f"Scraping complete. Results saved in '{self.output_file}'")
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")

    def run(self) -> None:
        """
        Main entry point to run the web scraping process. It loads the latest search results,
        scrapes the websites, and saves the scraped content.
        
        Raises:
            Exception: If any error occurs during the scraping process.
        """
        try:
            logger.info("Starting web scraping process.")
            results = self.load_latest_json()
            scraped_results = self.scrape_results(results)
            self.save_results(scraped_results)
        except Exception as e:
            logger.error(f"Error during scraping process: {str(e)}")
            raise
