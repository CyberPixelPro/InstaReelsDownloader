import httpx
import os
from bs4 import BeautifulSoup
import re

# Use a common browser user agent to mimic browser behavior.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}

async def fetch_video_page(url):
    print(f"Fetching page for URL: {url}")
    async with httpx.AsyncClient(headers=HEADERS) as client:
        response = await client.get(url)
        if response.status_code == 200:
            print(f"Page fetched successfully: {url}")
            return response.text
        else:
            print(f"Failed to fetch page, status code: {response.status_code}")
            return None

async def extract_video_url(page_content):
    if not page_content:
        print("No page content to extract video URL from.")
        return None

    print("Extracting video URL from page content.")
    soup = BeautifulSoup(page_content, 'html.parser')
    video_tag = soup.find('video')
    if video_tag and video_tag.get('src'):
        print(f"Found video URL: {video_tag.get('src')}")
        return video_tag.get('src')
    else:
        print("No video URL found in page content.")
        return None

async def download_video(video_url, destination='/cache'):
    if not video_url:
        print("No video URL provided to download.")
        return None

    print(f"Downloading video from URL: {video_url}")
    async with httpx.AsyncClient(headers=HEADERS) as client:
        response = await client.get(video_url)
        if response.status_code == 200:
            filename = os.path.join(destination, video_url.split('/')[-1])
            if not os.path.exists(destination):
                os.makedirs(destination)
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Video downloaded successfully: {filename}")
            return filename
        else:
            print(f"Failed to download video, status code: {response.status_code}")
            return None

async def download_reel(instagram_url):
    print(f"Starting download process for Instagram URL: {instagram_url}")
    page_content = await fetch_video_page(instagram_url)
    video_url = await extract_video_url(page_content)
    if video_url:
        return await download_video(video_url)
    else:
        print("Download process failed. No video was downloaded.")
        return None
