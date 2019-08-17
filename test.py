import hmac
import hashlib

uuid = "28001bae24614ee5bae1c2ca5328aabc"
api_key = "C69BAF41DA5ABD1FFEDC6D2FEA56B"
secret_key = "~d}$Q7$eIni=V)9\\RK/P.RM4;9[7|@/CA}b~OW!3?EV`:<>M7pddUBL5n|0/*Cn"
version = "2.2.0.0.1.1"
build_version = "42"
channel = 2
header = {
        "api-key": "C69BAF41DA5ABD1FFEDC6D2FEA56B",
        "accept": "application/vnd.picacomic.com.v1+json",
        "app-channel": channel,
        "time": 0,
        "nonce": uuid,
        "signature": "encrypt",
        "app-version": version,
        "app-uuid": "cb69a7aa-b9a8-3320-8cf1-74347e9ee979",
        "app-platform": "android",
        "app-build-version": build_version,
        "User-Agent": "okhttp/3.8.1"
}


def encrypt(url, ts, method):
    """

    :param url: 完整链接：https://picaapi.picacomic.com/auth/sign-in
    :param ts: 要和head里面的time一致, int(time.time())
    :param method: http请求方式: "GET" or "POST"
    :return: header["signature"]
    """
    raw = url.replace("https://picaapi.picacomic.com/", "") + str(ts) + uuid + method + api_key
    raw = raw.lower()
    hc = hmac.new(secret_key.encode(), digestmod=hashlib.sha256)
    hc.update(raw.encode())
    return hc.hexdigest()


if __name__ == "__main__":
    encrypt("https://picaapi.picacomic.com/announcements?page=1", 1533301254, 'GET')
