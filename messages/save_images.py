import os
import re
import requests

# Create the media folder if it doesn't exist
os.makedirs("media", exist_ok=True)

# List of files to process
file_paths = [
    "domains/cdn.discordapp.com.txt",
    "domains/images-ext-1.discordapp.net.txt",
    "domains/images-ext-2.discordapp.net.txt"
]

# Regular expression to find media links
media_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.mp4', '.mov', '.avi', '.webm')
media_regex = re.compile(r'https?://[^\s]+(?:' + '|'.join(re.escape(ext) for ext in media_extensions) + r')')

# Simulate a real browser with headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def download_media(url, total, current):
    try:
        filename = url.split("/")[-1]
        filepath = os.path.join("media", filename)
        
        # Skip if already downloaded
        if os.path.exists(filepath):
            print(f"[{current}/{total}] Already exists: {filename}")
            return
        
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"[{current}/{total}] Downloaded: {filename}")
    except Exception as e:
        print(f"[{current}/{total}] Failed to download {url}: {e}")

# Calculate total links and track progress
for file_path in file_paths:
    try:
        with open(file_path, "r") as f:
            content = f.read()
            matches = media_regex.findall(content)
            total_links = len(matches)
            for index, url in enumerate(matches, start=1):
                download_media(url, total_links, index)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
