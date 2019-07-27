import os
import json
path = "D:/pic/"
files = os.listdir(path)
# def deal(p):
# 	div = '<div><img src="{}"/></div>\n'
# 	res = ""
# 	for i in os.listdir(p):
# 		res += div.format(i)
        
		
try:
	json_data = json.load(open(path + "data.json", encoding="utf8"))
except:
	json_data = {}
# start = len(json_data)
# for i in files:
# 	if not os.path.isdir(path + i):
# 		continue
# 	try:
# 		int(i)
# 	except ValueError:
# 		os.rename(path + i, path + str(start))
# 		print("new")
# 		json_data.update({start: i})
# 		start += 1
# open(path + "data.json", "w",encoding="utf8").write(json.dumps(json_data))
per = '<div><a href="{}">{}</a></div>\n'
res = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n'
for i in json_data.keys():
	res += per.format(i, json_data[i])
print(res)
open(path + "index.html", "w", encoding="utf8").write(res)

for i in os.listdir(path):
	tmp = path + i
	res = '<meta name="viewport" content="width=device-width,initial-scale=1" />\n'
	if not os.path.isdir(tmp):
		continue
	for j in os.listdir(tmp):
		res += '<div><img src="{}"/></div>\n'.format("./" + j)
	open(tmp + "/index.html", "w", encoding="utf8").write(res)
