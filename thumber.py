import os
from pathlib import Path
import requests
import sys
import urllib.request

from bs4 import BeautifulSoup


def main():
    path = Path.cwd()
    download_folder = "thumber_downloads"
    url = str(sys.argv[1].strip())

    if not os.path.exists(path / download_folder):
        os.mkdir(path / download_folder)

    if not validate_url(url):
        sys.exit("ERROR: not an Youtube link")
    url = clean_url(url)

    with urllib.request.urlopen(url) as response:
        html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    filename = "thumb_" + soup.title.string

    for link in soup.find_all("link"):
        l = link.get("href")
        try:
            if "maxresdefault" in l:
                res = requests.get(l)
                if res.status_code:
                    with open(
                        path / download_folder / (filename.replace("/", "") + ".jpg"),
                        "wb",
                    ) as img:
                        img.write(res.content)
                break
        except TypeError:
            sys.exit("ERROR: can't download this thumb")


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
    t_indicator = "&t="
    list_indicator = "&list"

    if t_indicator in url:
        return url[: url.find(t_indicator)]
    elif list_indicator in url:
        return url[: url.find(list_indicator)]
    return str(url)


if __name__ == "__main__":
    main()
