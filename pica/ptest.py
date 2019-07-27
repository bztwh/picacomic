from urllib import request
import threading
import sqlite3
import json
import time
import os
import requests
s = requests.session()
files = "D:/pic/"
def down(key, num, name):
    url = "https://storage1.picacomic.com/static/" + key
    print(url)
    with open(files + name + "/{0}.{1}".format(num, key.split(".")[-1]), "wb") as tmp:
        while True:
            res = s.get(url, headers={"cookie": "__cfduid=d22ce56d20b1ef2ee045b9fd633e667801533260611",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"})
            if res.status_code == 200:
                break
            print(res.text)
            #     break
            # except Exception as e:
            #     print(e.)
            #     time.sleep(2)
        tmp.write(res.content)


db = sqlite3.connect("data.db")
cur = db.cursor()
res = cur.execute("select name,data from crew limit 500 offset 1;")
for i in res:
    print(i[0], end=" ")
    if i[1] is None:
        continue
    data = json.loads(i[1])
    num = 0
    try:
        os.mkdir(files + i[0])
    except FileExistsError:
        continue
    for j in data:
        threading.Thread(target=down, args=(j, num, i[0])).start()
        break
    print(" count=" + str(num))
    time.sleep(20)
    break
    
