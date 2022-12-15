import os
from pathlib import Path
import re
import requests
import sys
import urllib.request

from bs4 import BeautifulSoup

args = sys.argv

path = Path.home() / "Downloads"
filename = "thumb_1"

URL = sys.argv[1]

if len(sys.argv) == 4:
    filename = sys.argv[2] + '.jpg'
    path = sys.argv[3]
elif len(sys.argv) == 3:
    filename = sys.argv[2] + '.jpg'

with urllib.request.urlopen(URL) as response:
    html = response.read()

soup = BeautifulSoup(html, 'lxml')

for link in soup.find_all('link'):
    l = link.get('href')
    if re.search(r"maxresdefault", l):
        res = requests.get(l)
        if res.status_code:
            if os.path.exists(path / filename):
                filename = filename.split('_')
                new_filename = filename[0] + str(int(filename[1]) + 1)
                with open(path / (new_filename + '.jpg'), 'wb') as img:
                    img.write(res.content)
            else:
                with open(path / (filename + '.jpg'), 'wb') as img:
                    img.write(res.content)
        break
