# picacomic

- 批评某位开发者，居然用这个来牟利，不怕被请去喝茶，而且态度还极端恶劣。
- 隔壁被pica查水表了，我整理一下api

## 验证

``` golang

// header:
header := map[string]string{
    "api-key":           "C69BAF41DA5ABD1FFEDC6D2FEA56B",
    "accept":            "application/vnd.picacomic.com.v1+json",
    "app-channel":       "2",
    "time":              strconv.FormatInt(time.Now().Unix(), 10),
    "nonce":             "b1ab87b4800d4d4590a11701b8551afa",
    "signature":         "",
    "app-version":       "2.2.0.0.1.1",
    "app-uuid":          "cb69a7aa-b9a8-3320-8cf1-74347e9ee970",
    "app-platform":      "android",
    "app-build-version": "42",
    "Content-Type":      "application/json; charset=UTF-8",
    "User-Agent":        "okhttp/3.8.1",
    "authorization":     token,
    "image-quality":     "original",
}

func getSign(header map[string]string, url string, method string) map[string]string {
    var nonce = "b1ab87b4800d4d4590a11701b8551afa"
    var apiKey = "C69BAF41DA5ABD1FFEDC6D2FEA56B"
    var raw = strings.Replace(url, "https://picaapi.picacomic.com/",    "", 1) + header["time"] + nonce + method + apiKey
    raw = strings.ToLower(raw)
    h := hmac.New(sha256.New, []byte("~d}$Q7$eIni=V)9\\RK/P.RM4;9[7|@   CA}b~OW!3?EV`:<>M7pddUBL5n|0/*Cn"))
    h.Write([]byte(raw))
    header["signature"] = hex.EncodeToString(h.Sum(nil))
    return header
}
```

## Login

``` python
url: "https://picaapi.picacomic.com/auth/sign-in"
method: POST
body: {"email":"account","password":"password"}
response:
{
  "code": 200,
  "message": "success",
  "data": {
    "token": " " # 这个token放在headers的authorization就可以访问pica了
  }
}
```

## categories

``` python
url: "https://picaapi.picacomic.com/categories"
method: GET
response:
{
  "code": 200,
  "message": "success",
  "data": {
    "categories": [
      {
        "title": "援助嗶咔",
        "thumb": {
          "originalName": "help.jpg",
          "path": "help.jpg",
          "fileServer": "https://oc.woyeahgo.cf/static/"
        },
        "isWeb": true,
        "active": true,
        "link": "https://donate.woyeahgo.cf"
      },
      {
        "title": "嗶咔女皇總選",
        "thumb": {
          "originalName": "final-vote.jpeg",
          "path": "final-vote.jpeg",
          "fileServer": "https://oc.woyeahgo.cf/static/"
        },
        "isWeb": true,
        "active": true,
        "link": "https://final-vote.woyeahgo.cf"
      },
      {
        "title": "大家都在看",
        "thumb": {
          "originalName": "every-see.jpg",
          "path": "every-see.jpg",
          "fileServer": "https://oc.woyeahgo.cf/static/"
        },
        "isWeb": false,
        "active": true
      }, ....
    ]
  }
}

```
