import os
from pathlib import Path
import re
import requests
import sys
import urllib.request

from bs4 import BeautifulSoup


def validate_url(url):
    """
    Check if the URL passed to the program is from Youtube
    :param url: str
    :return: bool
    """
    if "youtu" not in url:
        return False
    return True


def clean_url(url):
    """
    Removes url indicators and returns the clean URL to the video
    :param url: str
    :return: str with the clean URL
    """
    time_indicator = "&t="
    playlist_indicator = "&list"

    if time_indicator in url:
        return url[:url.find(time_indicator)]
    if playlist_indicator in url:
        return url[:url.fin(playlist_indicator)]
    return url


def main():
    pass


args = sys.argv
DOWNLOAD_DIRECTORY = "thumb_downloads"
PARENT_DIRECTORY = Path.home() / "Pictures"
path = PARENT_DIRECTORY / DOWNLOAD_DIRECTORY

if not os.path.exists(path):
    os.mkdir(path)

filename = "thumb"
url = sys.argv[1].strip()

if validate_url(url):
    url = clean_url(url)
else:
    sys.exit("ERROR: this is not an Youtube link")


if len(sys.argv) == 4:
    filename = sys.argv[2] + '.jpg'
    path = Path(sys.argv[3])
elif len(sys.argv) == 3:
    filename = sys.argv[2] + '.jpg'


with urllib.request.urlopen(url) as response:
    html = response.read()

soup = BeautifulSoup(html, 'lxml')

for link in soup.find_all('link'):
    l = link.get('href')
    try:
        if re.search(r"maxresdefault", l):
            res = requests.get(l)
            if res.status_code:
                if not os.path.exists(path / (filename + '.jpg')):
                    with open(path / (filename + '.jpg'), 'wb') as img:
                        img.write(res.content)
                else:
                    new_filename = input("File already exists. Press ENTER to overwrite or choose a new name\n")
                    if new_filename == '':
                        with open(path / (filename + '.jpg'), 'wb') as img:
                            img.write(res.content)
                    else:
                        with open(path / (new_filename + '.jpg'), 'wb') as img:
                            img.write(res.content)
            sys.exit()
    except TypeError:
        sys.exit("Can't download this thumb")
