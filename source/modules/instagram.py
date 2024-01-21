import requests
from bs4 import BeautifulSoup
import re
import os

def modify_url(instagram_url):
    return instagram_url.replace('www.instagram.com', 'www.ddinstagram.com')

def extract_download_link(modified_url):
    response = requests.get(modified_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        video_tag = soup.find('a', href=re.compile(r'(.mp4)$'))

        if video_tag and 'href' in video_tag.attrs:
            return video_tag['href']
        else:
            return None
    else:
        return None

def download_video(video_url, destination_folder='/cache'):
    local_filename = os.path.join(destination_folder, video_url.split('/')[-1])
    with requests.get(video_url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def download_reel(instagram_url):
    modified_url = modify_url(instagram_url)
    download_link = extract_download_link(modified_url)
    if download_link:
        return download_video(download_link)
    else:
        return None
