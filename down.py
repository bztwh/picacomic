# import requests

# # res = requests.get("https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_ip.txt").text.split('\n')
# # for i in res:
# #     if len(i):
# #         print(i, end=',')
# url = "https://newsapi.sina.cn/?resource=hbpage&newsId=HB-1-snhs/index-search&lq=1&page=1&newpage=0&keyword=%25E9%25A3%259F%25E5%2593%2581&lDid=4ae20d66-5bba-45e5-9e85-4a0e0aa5e926&appVersion=7.13.0&oldChwm=12040_0007&city=CHXX0037&loginType=0&authToken=a664e1bbd64787befcdd01fea2bcde74&link&authGuid=6517733676825217781&ua=Xiaomi-Redmi+Note+5__sinanews__7.13.0__android__8.1.0&deviceId=5052b6ea05a270f4&connectionType=2&resolution=1080x2030&mac=02%3A00%3A00%3A00%3A00%3A00&weiboUid&osVersion=8.1.0&chwm=12040_0007&weiboSuid&andId=ad5f4505d726435d&from=6000095012&sn=b980400&aId=01AgCF2DAmG7vLqunDv5XCEcvM8E90Yk8yPNKdoSntFyu4DO0.&deviceIdV1=122bdc42a5562093&osSdk=27&abver=1553947583700130000&accessToken&seId=026e5da5cf&imei=861742041654968&deviceModel=Xiaomi__xiaomi__Redmi+Note+5&location=23.15292%2C113.367289&authUid=0&urlSign=d2ac47467e&rand=651"
# header = {
#         "Accept-Language": "zh-CN,zh;q=0.8",
#         "User-Agent": "Xiaomi-Redmi Note 5__sinanews__7.13.0__android__8.1.0",
#         "X-User-Agent": "Xiaomi-Redmi Note 5__sinanews__7.13.0__android__8.1.0",
#         "SN-REQID": "1553948895321bf15309a4910"
# }
# res = requests.get(url, headers=header).text
# print(res)
n = int(input())
s1 = input()
s2 = input()
a1=0
a2=0 
for i in s1:
    a1=(a1<<5)+ord(i)-ord('a')
for i in s2:
    a2=(a2<<5)+ord(i)-ord('a')

mid = (a1+a2)>>1
res = ""
while mid>0:
    res = chr(mid%26 + ord('a')) + res
    mid //= 26
deta = n-len(res)
while deta:
    deta -= 1
    res = 'a' + res
print(res)