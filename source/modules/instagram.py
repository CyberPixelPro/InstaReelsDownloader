import httpx
import os
from bs4 import BeautifulSoup
import re

async def modify_url(instagram_url):
    return instagram_url.replace('www.instagram.com', 'www.ddinstagram.com')

async def extract_download_link(client, modified_url):
    response = await client.get(modified_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        video_tag = soup.find('a', href=re.compile(r'(.mp4)$'))
        if video_tag and 'href' in video_tag.attrs:
            return video_tag['href']
        else:
            return None
    else:
        return None

async def download_video(client, video_url, destination_folder='/cache'):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    local_filename = os.path.join(destination_folder, video_url.split('/')[-1])
    response = await client.get(video_url)
    if response.status_code == 200:
        with open(local_filename, 'wb') as f:
            f.write(response.content)
        return local_filename
    else:
        return None

async def download_reel(instagram_url):
    async with httpx.AsyncClient() as client:
        modified_url = await modify_url(instagram_url)
        download_link = await extract_download_link(client, modified_url)
        if download_link:
            return await download_video(client, download_link)
        else:
            return None
