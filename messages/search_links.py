import csv
import requests
import logging
import re
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_first_url(text):
    """
    Extracts the first URL from a given text.

    Args:
        text (str): The input text.

    Returns:
        str or None: The first URL found, or None if no URL is present.
    """
    url_pattern = r'(https?://[^\s]+)'
    match = re.search(url_pattern, text)
    return match.group(0) if match else None

def is_file_url(url):
    """
    Checks if a URL points to a file.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL points to a file, False otherwise.
    """
    file_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip', '.rar', '.txt')
    return url.lower().endswith(file_extensions)

def download_file(url, date_str, output_dir):
    """
    Downloads a file from a URL and saves it with a date-based filename.

    Args:
        url (str): The file URL.
        date_str (str): The date string to use in the filename.
        output_dir (str): The directory to save the file.
    """
    try:
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200:
            file_extension = os.path.splitext(url)[-1]
            filename = f"{date_str}{file_extension}"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            logging.info(f"File downloaded: {filepath}")
        else:
            logging.warning(f"Failed to download file. Status code: {response.status_code}")
    except requests.RequestException as e:
        logging.error(f"Error downloading file: {url}. Error: {e}")

def write_url_to_domain_file(url, output_dir):
    """
    Writes a URL to a file named after its domain.

    Args:
        url (str): The URL to write.
        output_dir (str): The directory to save the domain file.
    """
    domain = urlparse(url).netloc
    domain_file = os.path.join(output_dir, f"{domain}.txt")
    with open(domain_file, 'a', encoding='utf-8') as file:
        file.write(url + '\n')
    logging.info(f"URL written to domain file: {domain_file}")

def check_url(url, headers, date_str, file_dir, domain_dir):
    """
    Checks if a URL is active and processes it accordingly.

    Args:
        url (str): The URL to check.
        headers (dict): Headers to simulate a real device.
        date_str (str): The date string for naming files.
        file_dir (str): Directory to save files.
        domain_dir (str): Directory to save domain files.

    Returns:
        str or None: The URL if active, otherwise None.
    """
    try:
        response = requests.head(url, headers=headers, timeout=5)
        if response.status_code == 200:
            logging.info(f"Active URL found: {url}")
            if is_file_url(url):
                download_file(url, date_str, file_dir)
            else:
                write_url_to_domain_file(url, domain_dir)
            return url
        else:
            logging.warning(f"URL returned status code {response.status_code}: {url}")
    except requests.RequestException as e:
        logging.error(f"Failed to connect to URL: {url}. Error: {e}")
    return None

def check_links_in_csv(csv_file_path, file_dir, domain_dir):
    """
    Reads a CSV file, checks for active links, downloads files, and sorts non-file URLs by domain.

    Args:
        csv_file_path (str): Path to the input CSV file.
        file_dir (str): Directory to save files.
        domain_dir (str): Directory to save domain files.
    """
    logging.info("Starting to process the CSV file.")
    os.makedirs(file_dir, exist_ok=True)
    os.makedirs(domain_dir, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    urls = []
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            for cell in row:
                url = extract_first_url(cell)
                if url:
                    urls.append((url, cell))

    total_urls = len(urls)
    logging.info(f"Found {total_urls} URLs to check.")

    with ThreadPoolExecutor() as executor:
        future_to_url = {
            executor.submit(
                check_url, url, headers, datetime.now().strftime('%Y-%m-%d'), file_dir, domain_dir
            ): url for url, _ in urls
        }
        for i, future in enumerate(as_completed(future_to_url), start=1):
            future.result()
            progress = (i / total_urls) * 100
            logging.info(f"Progress: {progress:.2f}%")

    logging.info("Finished processing the CSV file.")

if __name__ == "__main__":
    csv_file_path = "messages.csv"
    file_dir = "files"
    domain_dir = "domains"

    logging.info("Program started.")
    check_links_in_csv(csv_file_path, file_dir, domain_dir)
    logging.info("Processing complete.")