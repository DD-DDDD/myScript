#验证码的识别，为tesseract，需本地安装
import requests
from bs4 import BeautifulSoup
import subprocess
import time
import http.cookiejar as cookielib

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': '202.196.13.8:8080',
    'Origin': 'http://202.196.13.8:8080',
    'Referer': 'http://202.196.13.8:8080/reader/login.php',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    }

session = requests.Session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")


def get_captcha():
    captcha_url ="http://202.196.13.8:8080/reader/captcha.php"
    x = 0
    bin = session.get(captcha_url, headers=headers).content
    with open("d:/python/euler/%s.jpg" % x, "wb")as file:
        file.write(bin)
        file.close()

    p = subprocess.Popen(["tesseract", "d:/python/euler/0.jpg", "d:/python/euler/captcha"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    f = open("d:/python/euler/captcha.txt", "r")
    captchaResponse = f.read().replace(" ", " ").replace("\n", "")
    return captchaResponse


def login(xuehao, password):
    from_data = {
        'number': xuehao,
        'passwd': password,
        'captcha': get_captcha(),
        'select': 'cert_no',
        'returnUrl': '',
        }
    time.sleep(2)
    session.post("http://202.196.13.8:8080/reader/redr_verify.php", data=from_data, headers=headers)
    info = session.get("http://202.196.13.8:8080/reader/redr_info.php", headers=headers).content.decode("UTF-8")
    soup = BeautifulSoup(info, "lxml")
    print(soup)
    session.cookies.save()

if __name__ == '__main__':
    login("", "")
