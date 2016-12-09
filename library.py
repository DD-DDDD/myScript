import requests
from bs4 import BeautifulSoup
import subprocess
import time
import http.cookiejar as cookielib
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='jian',
                       port=3306, db='scraping', charset='utf8')
cur = conn.cursor()
cur.execute("use scraping")
cur.execute("create table yingshu_2015(条形码 INT(100), 书名 VARCHAR(200), 作者 VARCHAR(200), 借阅日期 DATE , 归还日期 DATE , 馆藏地 VARCHAR(200))")

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
    captcharesponse = f.read().replace(" ", " ").replace("\n", "")

    return captcharesponse


def login(xuehao):
    from_data = {
        'number': xuehao,
        'passwd': password,
        'captcha': get_captcha(),
        'select': 'cert_no',
        'returnUrl': '',
    }
    data = {
        'para_string': 'all',
        'topage': '1',
    }
    time.sleep(2)
    session.post("http://202.196.13.8:8080/reader/redr_verify.php", data=from_data, headers=headers)
    session.get("http://202.196.13.8:8080/reader/redr_info.php", headers=headers).content.decode("UTF-8")
    book_info = session.post("http://202.196.13.8:8080/reader/book_hist.php", headers=headers, data=data).content.decode("UTF-8")
    soup = BeautifulSoup(book_info, "lxml")
    book_info = soup.findAll("tr")
    for i in range(1, len(book_info)):
        print(book_info[i].get_text().split("\n"))
        cur.execute("insert into yingshu_2015(条形码, 书名, 作者, 借阅日期, 归还日期, 馆藏地) VALUES (%s, %s, %s, %s, %s, %s)", (book_info[i].get_text().split("\n")[2], book_info[i].get_text().split("\n")[3], book_info[i].get_text().split("\n")[4], book_info[i].get_text().split("\n")[5], book_info[i].get_text().split("\n")[6], book_info[i].get_text().split("\n")[7]))
        conn.commit()
    session.cookies.save()
if __name__ == '__main__':
        login("")
