import requests
import re
import time

# https://exhentai.org/api.php
# {"method": "gdata", "gidlist": [[1438102,"7450614e10"]], "namespace": 1}
s = requests.session()

def login(username, password):
    post_data = {
        'referer' : 'https://forums.e-hentai.org/index.php',
        'UserName' : username,
        'PassWord' : password,
        'CookieDate' : '1',
    }
    rs = s.post('https://forums.e-hentai.org/index.php?act=Login&CODE=01', post_data)

def pic(gid, token):
    url = "https://exhentai.org/g/{}/{}/?p=".format(gid, token)
    rs = s.get(url).text
    print(rs)
    page = max(list(map(int, re.findall("p=(\\d+)", rs))))
    picUrl = []
    for i in range(page + 1):
        tmpUrl = url + str(i)
        rs = s.get(tmpUrl).text
        urls = re.findall('https://exhentai.org/s/(.*?)"', rs)
        for j in urls:
            tmpUrl = "https://exhentai.org/s/" + j
            rs = s.get(tmpUrl).text
            pics = re.findall('img id="img" src="(.*?)"', rs)[0]
            print(pics)
            picUrl.append(pics)
            open("D:/pic/" + pics.split("/")[-1], "wb").write(s.get(pics).content)
            time.sleep(1)
    return picUrl

def getInfo(tokenList):
    url = "https://exhentai.org/api.php"
    data = {"method": "gdata", "gidlist": tokenList, "namespace": 1}
    rs = s.post(url, json=data).json()
    ret = []
    for i in rs["gmetadata"]:
        tmp = str(i["tags"]).lower()
        if "chinese" not in tmp or "3d" in tmp:
            continue
        tsTmp = {}
        tsTmp["title"] = i["title"]
        tsTmp["tags"] = i["tags"]
        tsTmp["count"] = i["filecount"]
        tsTmp["pid"] = i["thumb"].split("/")[6][:10]
        tsTmp["gid"], tsTmp["token"] = i["gid"], i["token"]
        ret.append(tsTmp.copy())
    return ret

def search(keyword, lowRad=2, page=1):
    url = "https://exhentai.org/"
    param = {
        "f_search": keyword,
        "advsearch": "1",
        "f_sname": "on",
        "f_stags": "on",
        "f_sr": "on",
        "f_srdd": lowRad,
        "f_spf": "",
        "f_spt": "",
        "page": page
    }
    rs = s.get(url=url, params=param).text
    rs = re.findall("/g/(.{18})", rs)
    ret = []
    for i in rs:
        i = i.split('/')
        ret.append(i)
    return ret

login("486994194", "486994194")
for k in range(23):
    rs = search("skinsuit", page=k)
    rs = getInfo(rs)
    for i in rs:
        pic(i["gid"], i["token"])
    time.sleep(2)
