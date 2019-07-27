import os
from flask import Flask, abort, redirect

path = "D:/pic/"
app = Flask(__name__)
file_list = os.listdir(path)

@app.route('/')
def root():
    cnt = 0
    body = """<html><body><table class="dataintable">{}</table></div></body></html>"""
    per = '<tr><td><a href="/book/{}">{}</a></td></tr>'
    res = ""
    for i in file_list:
        res += per.format(cnt, i)
        cnt += 1
    return body.format(res)

@app.route('/book/<int:page>')
def get_book(page):
    div = '<div><img src="/pic/{}/{}"/></div>\n'
    res = '<meta name="viewport" content="width=device-width,initial-scale=1" />\n'
    for i in os.listdir(path + file_list[page]):
        res += div.format(page, i)
    return res

@app.route('/pic/<int:page>/<name>')
def return_pic(page, name):
    with open(path + file_list[page] + '/' + name, "rb") as out:
        return out.read()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
