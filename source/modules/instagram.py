import httpx
from bs4 import BeautifulSoup
import os
from pathlib import Path
import re

# Define headers to mimic the browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Referer": "https://saveig.app/en",
}

async def fetch_content(url):
    print(f"Attempting to fetch content from URL: {url}")
    async with httpx.AsyncClient(headers=HEADERS) as client:
        resp = await client.get(url)
        if resp.status_code == 200:
            print("Content fetched successfully")
            return resp.text
        else:
            print(f"Failed to fetch content, status code: {resp.status_code}")
            return None

async def extract_video_url(html_content):
    print("Extracting video URL from the HTML content")
    soup = BeautifulSoup(html_content, 'html.parser')
    # Your extraction logic might vary, and you might need to adjust the following line:
    video_tag = soup.find('meta', attrs={'property': 'og:video'})
    if video_tag and video_tag.get('content'):
        video_url = video_tag['content']
        print(f"Extracted video URL: {video_url}")
        return video_url
    else:
        print("Could not find a video URL in the HTML content.")
        return None

async def download_video(url, destination_folder='/cache'):
    if not url:
        print("No URL provided to download.")
        return None
    
    print(f"Downloading video from URL: {url}")
    async with httpx.AsyncClient(headers=HEADERS) as client:
        resp = await client.get(url)
        if resp.status_code == 200:
            Path(destination_folder).mkdir(parents=True, exist_ok=True)
            filename = os.path.join(destination_folder, os.path.basename(url))
            with open(filename, 'wb') as file:
                file.write(resp.content)
            print(f"Video saved to: {filename}")
            return filename
        else:
            print(f"Failed to download the video, status code: {resp.status_code}")
            return None

async def download_reel(instagram_url):
    print(f"Starting the download process for Instagram URL: {instagram_url}")
    modified_url = instagram_url.replace("instagram.com", "ddinstagram.com")
    html_content = await fetch_content(modified_url)
    
    if html_content:
        video_url = await extract_video_url(html_content)
        if video_url:
            return await download_video(video_url)
        else:
            print("Video URL extraction failed.")
            return None
    else:
        print("Failed to fetch the page for the given Instagram URL.")
        return None


