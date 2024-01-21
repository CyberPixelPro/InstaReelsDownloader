import httpx
import os
from bs4 import BeautifulSoup
import re
from pathlib import Path

# Define headers that mimic a browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Referer": "https://saveig.app/en",
}

async def fetch_page_content(url):
    print(f"Fetching page content for URL: {url}")
    async with httpx.AsyncClient(headers=HEADERS) as client:
        response = await client.get(url)
        if response.status_code in [200, 302]:  # Check for success or redirect
            return response.text
        else:
            print(f"Failed to fetch page, status code: {response.status_code}")
            return None

async def extract_video_url(page_content):
    print("Extracting video URL from page content.")
    soup = BeautifulSoup(page_content, 'html.parser')
    script_tags = soup.find_all('script', type=lambda x: x and 'application/ld+json' in x)
    for script in script_tags:
        if 'video' in script.string:
            video_data = re.search(r'("contentUrl": ")(.*?mp4)', script.string)
            if video_data:
                video_url = video_data.group(2).replace('\\u0026', '&')
                print(f"Found video URL: {video_url}")
                return video_url
    print("No video URL found in page content.")
    return None

async def download_video(url, destination_folder='/cache'):
    if not url:
        print("No video URL provided for download.")
        return None

    print(f"Downloading video from URL: {url}")
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            # Create destination folder if it doesn't exist
            Path(destination_folder).mkdir(parents=True, exist_ok=True)
            # Derive filename from the URL and save the video content
            filename = os.path.join(destination_folder, os.path.basename(url))
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Video downloaded successfully: {filename}")
            return filename
        else:
            print(f"Failed to download video, status code: {response.status_code}")
            return None

async def download_reel(instagram_url):
    print(f"Starting download process for Instagram URL: {instagram_url}")
    page_content = await fetch_page_content(instagram_url)
    if page_content:
        video_url = await extract_video_url(page_content)
        if video_url:
            return await download_video(video_url)
    print("Download process failed. No video was downloaded.")
    return None
