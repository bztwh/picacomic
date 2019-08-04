import requests
import re
import os
import json
import platform
import time

api = "https://weiss-a.xyz/dnew.php?tag_id=40&category_id=0&search=&page={}"
path = "D:/pic/" if platform.system().startswith("Win") else "/mnt/usb/pic/"
s = requests.session()
s.get("https://weiss-a.xyz/dnew.php")

for i in range(1, 300):
    url = api.format(i)
    s.headers.update({"referer": url})
    rs = s.get(url).text
    ids = re.findall('ID=(\\d+)', rs)
    ids = list(set(ids))
    for j in ids:
        foderName = path + j + "/"
        pageUrl = "https://weiss-a.xyz/readOnline2.php?ID={}&host_id=0".format(j)
        rs = s.get(pageUrl).text
        picJson = re.findall("Original_Image_List = (.*?);", rs)
        try:
            os.mkdir(foderName)
        except FileExistsError:
            pass
        if len(picJson) > 1:
            picJson = picJson[1]
        else:
            picJson = picJson[0]
        urlPre = re.findall('HTTP_IMAGE = "(.*?)"', rs)[0]
        picJson = json.loads(picJson)
        for k in picJson:
            fileName = foderName + k["sort"] + "." + k["extension"]
            if os.path.exists(fileName) and os.path.getsize(fileName) != 0:
                continue
            imgUrl = urlPre + k["new_filename"] + "_w1500." + k["extension"]
            content = s.get(imgUrl).content
            open(fileName, "wb").write(content)
        time.sleep(30)
