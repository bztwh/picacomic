import requests
import re
from xmlrpc import client
import time
api = "http://hentaiplay.net/hentai/episodes/uncensored/page/{}/"

s = requests.session()
ss = client.ServerProxy("http://127.0.0.1:6800/rpc")

def download(url):
    opt = dict(header=["User-Agent: okhttp/3.7.0"])
    return ss.aria2.addUri([url], opt)

def tell_status(guid):
    return ss.aria2.tellStatus(str(guid))

for i in range(1, 10):
    url = api.format(i)
    rs = s.get(url).text
    ep = re.findall('href="(.*?)" rel="bookmark"', rs)
    ep = list(set(ep))
    for i in ep:
        rs = s.get(i).text
        url = re.findall('src="(.*?)" type="video/mp4"', rs)[0]
        guid = download(url)
        while tell_status(guid)['status'] != 'complete':
            time.sleep(10)
