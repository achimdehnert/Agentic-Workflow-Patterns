from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from selenium.webdriver.common.by import By
from src.config.logging import logger
from urllib.parse import urlparse
from selenium import webdriver
from typing import Tuple, Dict, List, Any
import json
import time
import os
import re


class WebScraper:
    """
    A class to handle the setup, execution, and management of web scraping tasks.
    """

    INPUT_DIR = "./data/patterns/web_search/output/search"
    OUTPUT_DIR = "./scraped_content"
    OUTPUT_FILE = "scraped_content.txt"
    MAX_WORKERS = 5
    DRIVER_WAIT_TIME = 10

    def __init__(self, input_dir: str = INPUT_DIR, output_dir: str = OUTPUT_DIR, output_file: str = OUTPUT_FILE, max_workers: int = MAX_WORKERS):
        """
        Initializes the WebScraper with specified directories, output file, and number of workers.
        
        Args:
            input_dir (str): Directory where JSON files with search results are stored.
            output_dir (str): Directory where scraped content will be saved.
            output_file (str): File name where scraped content will be saved.
            max_workers (int): Maximum number of concurrent threads for scraping.
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.output_file = os.path.join(output_dir, output_file)
        self.max_workers = max_workers

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Cleans the input text by removing extra whitespace and newlines.
        
        Args:
            text (str): The text to be cleaned.
        
        Returns:
            str: The cleaned text.
        """
        return re.sub(r'\s+', ' ', text).strip()

    @staticmethod
    def get_domain(url: str) -> str:
        """
        Extracts the domain from a given URL.
        
        Args:
            url (str): The URL from which the domain is to be extracted.
        
        Returns:
            str: The domain of the URL.
        """
        return urlparse(url).netloc

    @staticmethod
    def setup_driver() -> webdriver.Chrome:
        """
        Sets up and returns a headless Chrome WebDriver.
        
        Returns:
            webdriver.Chrome: An instance of Chrome WebDriver.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    def scrape_website(self, url: str, driver: webdriver.Chrome) -> str:
        """
        Scrapes text content from the specified website using the provided WebDriver.
        
        Args:
            url (str): The URL of the website to scrape.
            driver (webdriver.Chrome): The WebDriver instance to use for scraping.
        
        Returns:
            str: The cleaned text content from the website.
        """
        try:
            driver.get(url)
            WebDriverWait(driver, self.DRIVER_WAIT_TIME).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            elements = driver.find_elements(By.CSS_SELECTOR, "p, h1, h2, h3, h4, h5, h6")
            text = ' '.join([elem.text for elem in elements])
            return self.clean_text(text)
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return ""

    def scrape_with_delay(self, result: Dict[str, Any], driver: webdriver.Chrome, delay: int) -> Tuple[Dict[str, Any], str]:
        """
        Scrapes the website after a specified delay.
        
        Args:
            result (Dict[str, Any]): The result dictionary containing the URL and other metadata.
            driver (webdriver.Chrome): The WebDriver instance to use for scraping.
            delay (int): The delay in seconds before starting the scraping.
        
        Returns:
            Tuple[Dict[str, Any], str]: The result metadata and the scraped content.
        """
        time.sleep(delay)
        content = self.scrape_website(result['Link'], driver)
        return result, content

    def load_latest_json(self) -> List[Dict[str, Any]]:
        """
        Loads the most recent JSON file from the input directory.
        
        Returns:
            List[Dict[str, Any]]: A list of results from the latest JSON file.
        
        Raises:
            FileNotFoundError: If no JSON files are found in the input directory.
        """
        json_files = [f for f in os.listdir(self.input_dir) if f.endswith('.json')]
        if not json_files:
            raise FileNotFoundError("No JSON files found in the input directory.")
        
        latest_file = max(json_files, key=lambda f: os.path.getmtime(os.path.join(self.input_dir, f)))
        with open(os.path.join(self.input_dir, latest_file), 'r') as f:
            data = json.load(f)
        
        return data['Top Results']

    def scrape_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Scrapes all the provided results concurrently and returns the scraped content.
        
        Args:
            results (List[Dict[str, Any]]): A list of results containing URLs to scrape.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the title, URL, snippet, and scraped content.
        """
        os.makedirs(self.output_dir, exist_ok=True)
        drivers = [self.setup_driver() for _ in range(min(self.max_workers, len(results)))]

        scraped_results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_result = {
                executor.submit(self.scrape_with_delay, result, drivers[i % len(drivers)], i): result
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

        for driver in drivers:
            driver.quit()

        return scraped_results

    def save_results(self, scraped_results: List[Dict[str, Any]]) -> None:
        """
        Saves the scraped results to a specified output file.
        
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
        Executes the full web scraping process from loading data to saving results.
        """
        try:
            results = self.load_latest_json()
            scraped_results = self.scrape_results(results)
            self.save_results(scraped_results)
        except Exception as e:
            logger.error(f"Error during scraping process: {str(e)}")


if __name__ == "__main__":
    scraper = WebScraper()
    scraper.run()
