import requests

url = "https://login.51job.com/login.php?lang=c"

post_data = {'lang':        'c',
             'action':      'save',
             'from_domain': 'i',
             'loginname':   '保密',
             'password':    "保密",
             'verifycode':  '',
             'isread':      'on'

             }
headers = {
    'Connection':                "keep-alive",
    'Cache-Control':             "no-cache",
    'Origin':                    "https://login.51job.com",
    'Upgrade-Insecure-Requests': "1",
    'Content-Type':              "application/x-www-form-urlencoded",
    'User-Agent':                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
    'Accept':                    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Referer':                   "https://login.51job.com/login.php?lang=c",
    'Accept-Encoding':           "gzip, deflate, br",
    'Accept-Language':           "zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6"
}

s = requests.session()

response = requests.request("POST", url, data=post_data, headers=headers, )
response.encoding = 'gbk'

print(response.status_code)
print(response.text)
