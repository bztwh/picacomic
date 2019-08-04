import requests
import platform
import os
import re
import json
import time
api = "https://hentai.cafe/page/{}/"

path = "D:/pic/" if platform.system().startswith("Win") else "/mnt/usb/pic/"
s = requests.session()

for i in range(1, 400):
    url = api.format(i)
    rs = s.get(url).text
    pageUrl = re.findall('"(.*?)" class="entry-thumb', rs)
    for j in pageUrl:
        folderName = j.split("/")[3] + "/"
        absolute = path + folderName
        try:
            os.mkdir(absolute)
        except FileExistsError:
            pass
        rs = s.get(j).text
        viewUrl = re.findall('href="(.*?)" title="Read"', rs)[0]
        rs = s.get(viewUrl).text
        imgJson = re.findall('var pages = (.*?);', rs)[0]
        imgJson = json.loads(imgJson)
        for k in imgJson:
            fileName = absolute + k["filename"]
            if os.path.exists(fileName) and os.path.getsize(fileName) != 0:
                continue
            content = s.get(k["url"]).content
            open(fileName, "wb").write(content)
        time.sleep(30)
        # break

