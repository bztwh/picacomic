# -*- coding: utf-8 -*-
import requests
import sqlite3
import time

inDb = sqlite3.connect("data.db")
inCur = inDb.cursor()
outDb = sqlite3.connect("file.db")
outCur = outDb.cursor()

data = inCur.execute("select id,pages from crew2").fetchall()
for i in data:
    idd, pages = i
    try:
        outCur.execute("create table id{}(id integer primary key, data blob)".format(idd))
    except Exception as e:
        print(e)
    print(idd, i)
    for j in range(1, pages + 1):
        sql = "select count(id) from id{} where id={}".format(idd, j)
        cnt = outCur.execute(sql).fetchone()[0]
        cnt = int(cnt)
        if cnt != 0:
            continue
        url = "https://bbs.gent41.com/g-meta-srv/img/{}/{}/{}.webp".format(idd//1000, idd, j)
        tryCnt = 0
        while True:
            try:
                res = requests.get(url)
                if res.status_code == 200:
                    break
            except Exception as e:
                print(e)
            time.sleep(2)
            tryCnt += 1
            if tryCnt >= 10:
                outDb.commit()
                raise Exception("MiaoMiaoMiao????")
        res = res.content
        sql = "insert into id{}(id,data)values(?,?)".format(idd)
        outCur.execute(sql, (j, sqlite3.Binary(res)))
        if j % 20 == 0:
            outDb.commit()
    outDb.commit()

