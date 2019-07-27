import requests
import re
import time
import sqlite3
import logging
import json
from urllib import parse

logging.basicConfig(filename='gen.log',
                    level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
                    datefmt='%m-%d %H:%M:%S',
                    filemode="w")

db = sqlite3.connect("data.db")
cur = db.cursor()
sstart = 23232

def communicate_db(sql):
    global cur
    try:
        __res = cur.execute(sql).fetchall()
        logging.info(str(__res))
        db.commit()
        return __res
    except (sqlite3.OperationalError, sqlite3.IntegrityError):
        return []

def get():
    url = "https://bbs.gent41.com/viewtopic.php?t="
    # start = int(communicate_db("select count(id) from crew2;")[0][0]) + 26
    global sstart
    for i in range(sstart, 35000):
        sstart = i
        tmp_url = url + str(i)
        res = requests.get(tmp_url)
        if res.status_code != 200:
            logging.info("{},{}".format(i, "not found"))
            continue
        res = res.text
        name = re.findall("<title>(.*?)- Gentai</title>", res)[0]
        pId = re.findall("img/\\d+/(\\d+)/", res)
        if len(pId) == 0:
            continue
        else:
            pId = pId[0]
        page = re.findall("start=(\\d+)", res)
        tags = re.findall("text = '(.*?)'", res)
        if len(tags) == 0:
            try:
                tags = re.findall('alt="图片"><br>([^<]+)', res)[0].strip()
            except IndexError:
                tags = ""
        else:
            tags = tags[0]
        if len(page) == 0:
            page = 0
        else:
            page = max(list(map(int, page)))
        while True:
            try:
                res = requests.get(tmp_url + "&start=" + str(page)).text
                total = max(list(map(int, re.findall("/g-meta-srv/img/\\d+/\\d+/(\\d+)", res))))
                break
            except ValueError:
                page -= 10
        communicate_db("insert into crew2(id, name, pages, tags) values({},'{}',{}, '{}')".format(pId, name, total, tags))
        logging.info("{},{},{},{},{}".format(i, pId, name, total, tags))

if __name__ == "__main__":
    while True:
        try:
            get()
            break
        except Exception as e:
            logging.error(str(e))
            time.sleep(120)
