import re
import requests
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup

DEFAULT_PATH = Path("C:\\Users\\fredm\\Downloads")
URL = "https://www.youtube.com/watch?v=MDJC16ShEDM"

with urllib.request.urlopen(URL) as response:
    html = response.read()

soup = BeautifulSoup(html, 'lxml')

for link in soup.find_all('link'):
    l = link.get('href')
    if re.search(r"maxresdefault", l):
        res = requests.get(l)
        if res.status_code:
            with open(DEFAULT_PATH / 'image_2.jpg', 'wb') as img:
                img.write(res.content)
        break
