import requests
from xmlrpc import client
import time
api = "https://hanime.tv/api/v3/browse/trending?time=month&page={}"
s = requests.session()
ss = client.ServerProxy("http://127.0.0.1:6800/rpc")

def download(url):
    opt = dict(header=["User-Agent: okhttp/3.7.0"])
    return ss.aria2.addUri([url], opt)

def tell_status(guid):
    return ss.aria2.tellStatus(str(guid))


s.headers.update({
    "Origin": "https://hanime.tv",
    "X-Directive": "api",
    "X-Session-Token": "",
    "X-Signature": "",
    "X-Time": "",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
})
print(s.headers)
for i in range(92):
    url = api.format(i)
    rs = s.get(url).json()
    for i in rs["hentai_videos"]:
        url2 = "https://members.hanime.tv/api/v3/videos_manifests/" + i["slug"]
        js = s.get(url2).json()["videos_manifest"]["servers"]
        flag = False
        for j in js:
            for k in j["streams"]:
                if k["extension"] != "m3u8" and int(k["height"]) < 1080:
                    guid = download(k["url"])
                    flag = True
                    while tell_status(guid)['status'] != 'complete':
                        time.sleep(10)
                    break
            if flag:
                time.sleep(60)
                break

