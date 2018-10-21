import requests

url = "https://dig.chouti.com/login"

payload = {
    'phone':    '',
    'password': '',
    'oneMonth': 1}
headers = {
    'cookie':           "gpsd=3c092ad0f0708f380e39ca53104f3d87; JSESSIONID=aaa1URqLL3w9_dsdLjYww; gpid=e7c8794cf22a48989650329ad13ec0ff; puid=cdu_53641499343",
    'origin':           "https://dig.chouti.com",
    'accept-encoding':  "gzip, deflate, br",
    'accept-language':  "zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6",
    'user-agent':       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
    'content-type':     "application/x-www-form-urlencoded; charset=UTF-8",
    'accept':           "*/*",
    'referer':          "https://dig.chouti.com/",
    'authority':        "dig.chouti.com",
    'x-requested-with': "XMLHttpRequest",
    'Cache-Control':    "no-cache",
    'Postman-Token':    "455a5875-416f-4778-974f-ad5e3fc6cb82"
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.status_code)
print(response.text)
