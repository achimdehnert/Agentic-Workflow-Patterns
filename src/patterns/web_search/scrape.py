from src.patterns.web_search.tasks import ScrapeTask
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from src.config.logging import logger
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from typing import Tuple
from typing import Dict
from typing import List 
from typing import Any 
import requests
import hashlib
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


    def generate_filename(self, query: str) -> str:
        """Generate a unique filename based on the query and location."""
        combined = f"{query}".encode('utf-8')
        return f"search_results_{hashlib.md5(combined).hexdigest()}.json"
    
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
        Scrapes the given website URL and extracts relevant content. If the request takes longer than 5 seconds,
        the website is skipped.
        
        Args:
            url (str): The URL to be scraped.
        
        Returns:
            str: Extracted text content from the webpage, or an empty string in case of an error.
        """
        try:
            response = requests.get(url, timeout=5)  # Adding a timeout of 5 seconds
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            extracted_text = ' '.join([elem.get_text() for elem in text_elements])
            return self.clean_text(extracted_text)
        except requests.Timeout:
            logger.warning(f"Skipping {url} due to timeout (more than 5 seconds)")
            return ""
        except requests.RequestException as e:
            logger.warning(f"Error scraping {url}: {str(e)}")
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
            # Adding a 3-second delay after saving results
            time.sleep(3)
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")


    def load_search_results(self, query: str, location: str) -> List[Dict[str, Any]]:
        try:
            filename = self.generate_filename(query)
            file_path = os.path.join(self.INPUT_DIR, filename)
            print('----------->', file_path)
            
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Search results file not found for query: '{query}' and location: '{location}'")
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            logger.info(f"Loaded search results from: {filename}")
            return data['Top Results']
        except Exception as e:
            logger.error(f"Error loading search results file: {str(e)}")
            raise


    def run(self, query: str, location: str) -> None:
        try:
            logger.info(f"Starting web scraping process for query: '{query}' and location: '{location}'")
            results = self.load_search_results(query, location)
            scraped_results = self.scrape_results(results)
            self.save_results(scraped_results)
        except Exception as e:
            logger.error(f"Error during scraping process: {str(e)}")
            raise
