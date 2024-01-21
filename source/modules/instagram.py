import httpx
import os
from bs4 import BeautifulSoup
import re

async def modify_url(instagram_url):
    modified_url = instagram_url.replace('www.instagram.com', 'www.ddinstagram.com')
    print(f"Modified URL: {modified_url}")  # Debugging
    return modified_url

async def extract_download_link(client, modified_url):
    try:
        response = await client.get(modified_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            video_tag = soup.find('a', href=re.compile(r'(.mp4)$'))
            if video_tag and 'href' in video_tag.attrs:
                print(f"Found video URL: {video_tag['href']}")  # Debugging
                return video_tag['href']
            else:
                print("No video URL found")  # Debugging
                return None
        else:
            print(f"Failed to fetch modified URL: Status code {response.status_code}")  # Debugging
            return None
    except Exception as e:
        print(f"Error in extract_download_link: {e}")  # Debugging
        return None

async def download_video(client, video_url, destination_folder='/cache'):
    try:
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        local_filename = os.path.join(destination_folder, video_url.split('/')[-1])
        response = await client.get(video_url)
        if response.status_code == 200:
            with open(local_filename, 'wb') as f:
                f.write(response.content)
            print(f"Video downloaded: {local_filename}")  # Debugging
            return local_filename
        else:
            print(f"Failed to download video: Status code {response.status_code}")  # Debugging
            return None
    except Exception as e:
        print(f"Error in download_video: {e}")  # Debugging
        return None

async def download_reel(instagram_url):
    try:
        async with httpx.AsyncClient() as client:
            modified_url = await modify_url(instagram_url)
            download_link = await extract_download_link(client, modified_url)
            if download_link:
                return await download_video(client, download_link)
            else:
                print("Download link not found")  # Debugging
                return None
    except Exception as e:
        print(f"Error in download_reel: {e}")  # Debugging
        return None


