from concurrent.futures import ThreadPoolExecutor, as_completed
from src.config.logging import logger
from typing import Tuple, Dict, List, Any
import json
import time
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re


class WebScraper:
    INPUT_DIR = "./data/patterns/web_search/output/search"
    OUTPUT_DIR = "./data/patterns/web_search/output/scrape"
    OUTPUT_FILE = "scraped_content.txt"
    MAX_WORKERS = 5

    def __init__(self, input_dir: str = INPUT_DIR, output_dir: str = OUTPUT_DIR, output_file: str = OUTPUT_FILE, max_workers: int = MAX_WORKERS):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.output_file = os.path.join(output_dir, output_file)
        self.max_workers = max_workers

    @staticmethod
    def clean_text(text: str) -> str:
        return re.sub(r'\s+', ' ', text).strip()

    @staticmethod
    def get_domain(url: str) -> str:
        return urlparse(url).netloc

    def scrape_website(self, url: str) -> str:
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            extracted_text = ' '.join([elem.get_text() for elem in text_elements])

            return self.clean_text(extracted_text)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return ""
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return ""

    def scrape_with_delay(self, result: Dict[str, Any], delay: int) -> Tuple[Dict[str, Any], str]:
        time.sleep(delay)
        content = self.scrape_website(result['Link'])
        return result, content

    def load_latest_json(self) -> List[Dict[str, Any]]:
        json_files = [f for f in os.listdir(self.input_dir) if f.endswith('.json')]
        if not json_files:
            raise FileNotFoundError("No JSON files found in the input directory.")

        latest_file = max(json_files, key=lambda f: os.path.getmtime(os.path.join(self.input_dir, f)))
        with open(os.path.join(self.input_dir, latest_file), 'r') as f:
            data = json.load(f)

        return data['Top Results']

    def scrape_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        os.makedirs(self.output_dir, exist_ok=True)

        scraped_results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
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
        try:
            results = self.load_latest_json()
            scraped_results = self.scrape_results(results)
            self.save_results(scraped_results)
        except Exception as e:
            logger.error(f"Error during scraping process: {str(e)}")
            raise


if __name__ == "__main__":
    scraper = WebScraper()
    scraper.run()