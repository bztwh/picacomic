import json
from flask import Flask, abort, redirect, request
import sqlite3
from urllib import parse
app = Flask(__name__)


@app.route('/')
def home():
    print(request.headers)
    return '<div><a href="gen/0">gentai</a></div>\n<div><a href="pica/0">pica</a></div>\n'


@app.route('/pica/<int:page>')
def pages(page):
    db = sqlite3.connect("data.db")
    cur = db.cursor()
    ans = cur.execute("select id,name from crew limit 50 offset {};".format(page * 50)).fetchall()
    per = '<div><a href="/pica/id/{}">{}</a></div>\n'
    res = ""
    for _ in ans:
        res += per.format(_[0], _[1])
    if page >= 1:
        res += '<div><a href="/pica/{}">last Page</a></div>\n'.format(page - 1)
    if len(ans):
        res += '<div><a href="/pica/{}">next Page</a></div>\n'.format(page + 1)
    return res


@app.route('/pica/id/<book_id>')
def getbook(book_id):
    if book_id == "favicon.ico":
        abort(404)
        return
    db = sqlite3.connect("data.db")
    cur = db.cursor()
    ans = cur.execute("select data from crew where id='{}';".format(book_id)).fetchone()
    if book_id == "favicon.ico" or ans is None:
        abort(404)
        return
    div = '<div><img src="https://s3.picacomic.com/static/{}"/></div>\n'
    ans = json.loads(ans[0])
    res = '<meta name="viewport" content="width=device-width,initial-scale=1" />\n'
    for _ in ans:
        res += div.format(_)
    return res

@app.route('/gen/<int:page>')
def pages2(page):
    db = sqlite3.connect("data.db")
    cur = db.cursor()
    ans = cur.execute("select id,name from crew2 limit 50 offset {};".format(page * 50)).fetchall()
    per = '<div><a href="/gen/id/{}">{}</a></div>\n'
    res = ""
    for _ in ans:
        res += per.format(_[0], _[1])
    if page >= 1:
        res += '<div><a href="/gen/{}">last Page</a></div>\n'.format(page - 1)
    if len(ans):
        res += '<div><a href="/gen/{}">next Page</a></div>\n'.format(page + 1)
    return res

board = """
<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <title>hello word</title>
    <script src="https://bbs.gent41.com/assets/javascript/libwebp.js"></script>
</head>

<body>
    <script>
        var tmp = {1};
        var id = {2};
        for (var i = 1; i <= tmp; i++) {
            document.write('<img id="' + i + '">');
        }
        for (var i = 1; i <= tmp; i++) {
            var srcs = 'https://bbs.gent41.com/g-meta-srv/img/' + Math.floor(id / 1000) + '/' + id + '/' + i + '.webp';
            loadWebP(document.getElementById('' + i), srcs);
        }
    </script>
</body>

</html>
"""

@app.route('/gen/id/<book_id>')
def getbook2(book_id):
    if book_id == "favicon.ico":
        abort(404)
        return
    db = sqlite3.connect("data.db")
    cur = db.cursor()
    ans = cur.execute("select id,pages from crew2 where id='{}';".format(book_id)).fetchone()
    if book_id == "favicon.ico" or ans is None:
        abort(404)
        return
    pId, page = ans[0], int(ans[1])

    return board.replace("{1}", str(page)).replace("{2}", str(pId))

@app.route('/s/<key>')
def search(key):
    key = parse.unquote(key)
    db = sqlite3.connect("data.db")
    cur = db.cursor()
    ans = cur.execute("select id,name from crew where name like '%{}%';".format(key))
    per = '<div><a href="/pica/id/{}">{}</a></div>\n'
    res = ""
    for _ in ans:
        res += per.format(_[0], _[1])
    ans = cur.execute("select id,name from crew2 where name like '%{}%';".format(key))
    per = '<div><a href="/gen/id/{}">{}</a></div>\n'
    res = ""
    for _ in ans:
        res += per.format(_[0], _[1])
    # if page >= 1:
    #     res += '<div><a href="/pica/{}">last Page</a></div>\n'.format(page - 1)
    # if len(ans):
    #     res += '<div><a href="/pica/{}">next Page</a></div>\n'.format(page + 1)
    return res

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
