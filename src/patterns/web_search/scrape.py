import json
import re
import time
import os
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def clean_text(text):
    # Remove extra whitespace and newlines
    return re.sub(r'\s+', ' ', text).strip()

def get_domain(url):
    return urlparse(url).netloc

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_website(url, driver):
    try:
        driver.get(url)
        
        # Wait for the body to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Get text from paragraph and header tags
        elements = driver.find_elements(By.CSS_SELECTOR, "p, h1, h2, h3, h4, h5, h6")
        text = ' '.join([elem.text for elem in elements])
        
        return clean_text(text)
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return ""

def scrape_with_delay(result, driver, delay):
    time.sleep(delay)
    content = scrape_website(result['Link'], driver)
    return result, content

def main():
    # Set the input directory
    input_dir = "./data/patterns/web_search/output/search"
    
    # Find the most recent JSON file in the input directory
    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
    if not json_files:
        print("No JSON files found in the input directory.")
        return
    
    latest_file = max(json_files, key=lambda f: os.path.getmtime(os.path.join(input_dir, f)))
    input_file = os.path.join(input_dir, latest_file)
    
    # Load JSON data
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    results = data['Top Results']
    
    # Create a directory for individual files
    os.makedirs('scraped_content', exist_ok=True)
    
    # Set up a pool of drivers
    num_workers = min(5, len(results))  # Use up to 5 workers
    drivers = [setup_driver() for _ in range(num_workers)]
    
    # Use ThreadPoolExecutor for concurrent scraping
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_result = {executor.submit(scrape_with_delay, result, drivers[i % num_workers], i): result 
                            for i, result in enumerate(results)}
        
        scraped_results = []
        for future in as_completed(future_to_result):
            result, content = future.result()
            title = result['Title']
            url = result['Link']
            snippet = result['Snippet']
            
            # Skip if no content was scraped
            if not content:
                print(f"Skipping {title} due to no content")
                continue
            
            scraped_results.append({
                'title': title,
                'url': url,
                'snippet': snippet,
                'content': content
            })
            
            print(f"Scraped: {title}")
    
    # Close all drivers
    for driver in drivers:
        driver.quit()
    
    # Write all non-empty results to a single file
    with open('scraped_content.txt', 'w', encoding='utf-8') as outfile:
        for result in scraped_results:
            outfile.write(f"==== BEGIN ENTRY ====\n")
            outfile.write(f"TITLE: {result['title']}\n")
            outfile.write(f"URL: {result['url']}\n")
            outfile.write(f"SNIPPET: {result['snippet']}\n")
            outfile.write(f"CONTENT:\n{result['content']}\n")
            outfile.write(f"==== END ENTRY ====\n\n")
    
    print("Scraping complete. Results saved in 'scraped_content.txt'")

if __name__ == "__main__":
    main()