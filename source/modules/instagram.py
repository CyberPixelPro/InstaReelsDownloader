import requests
from bs4 import BeautifulSoup
import re
import os

def modify_url(instagram_url):
    """
    Modify the Instagram URL to use the third-party service.
    """
    return instagram_url.replace('www.instagram.com', 'www.ddinstagram.com')

def extract_download_link(modified_url):
    """
    Extract the actual download link from the third-party service's page.
    """
    response = requests.get(modified_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # The exact extraction logic will depend on the third-party page's structure
        # You need to inspect the HTML to find out how to extract the video URL
        video_url = soup.find('a', href=re.compile(r'(.mp4)$'))['href']
        return video_url
    else:
        return None

def download_video(video_url, destination_folder='/path/to/download/folder'):
    """
    Download the video from the provided URL.
    """
    local_filename = os.path.join(destination_folder, video_url.split('/')[-1])
    with requests.get(video_url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def download_reel(instagram_url):
    """
    Main function to handle the download of an Instagram Reel.
    """
    modified_url = modify_url(instagram_url)
    download_link = extract_download_link(modified_url)
    if download_link:
        return download_video(download_link)
    else:
        return None
