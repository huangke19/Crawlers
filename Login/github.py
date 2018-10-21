''' 模拟登录Github，注意session要保持为同一个 '''

import re
import requests

username = input("username: ")
password = input("password: ")

headers = {
    'Referer':    'https://github.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Host':       'github.com'
}

s = requests.Session()
get_url = 'https://github.com/login'
login_url = 'https://github.com/session'

def get_cookie_and_token(url):
    global s
    res = s.get(url, headers=headers)
    pattern = re.compile('<input type="hidden" name="authenticity_token" value="(.*?)"', re.S)
    token = re.findall(pattern, res.text)[0]
    return token

def login(url, token):
    global s
    post_data = {
        'commit':             'Sign in',
        'utf8':               '✓',
        'authenticity_token': token,
        'login':              username,
        'password':           password
    }
    r = s.post(url, headers=headers, data=post_data)
    check_pattern = re.compile('<meta name="user-login" content="(.*?)">', re.S)
    name = re.findall(check_pattern, r.text)[0]
    if name == username:
        print('成功登录！')
    return name == username

def main():
    token = get_cookie_and_token(get_url)
    login_status = login(login_url, token)
    print(login_status)

if __name__ == '__main__':
    main()
