import requests
from selenium import webdriver

username = input('enter your username: ')
password = input('enter your password: ')

browser = webdriver.Chrome()
url = 'https://passport.lagou.com/login/login.html'
browser.get(url)

username_box = browser.find_element_by_xpath('//input[@placeholder="请输入常用手机号/邮箱"]')
username_box.send_keys(username)

password_box = browser.find_element_by_css_selector('input[placeholder="请输入密码"]')
password_box.send_keys(password)

login_btn = browser.find_element_by_xpath('/html/body/section/div[1]/div[2]/form/div[5]/input')
login_btn.click()

# 将selenium的cookie传给requests
req = requests.Session()
cookies = browser.get_cookies()
for cookie in cookies:
    req.cookies.set(cookie['name'], cookie['value'])
