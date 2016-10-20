import pymysql
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random
conn = pymysql.connect(host='localhost', user='root', password='jian',
                       port=3306, db='scraping', charset='utf8')

cur = conn.cursor()
cur.execute('use scraping')
random.seed(datetime.datetime.now())


def store(title, content):
    cur.execute("insert into pages (title, content) values (\"%s\", \"%s\")", (title, content))
    # 将title content放入pages表中
    cur.connection.commit()


def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bs0bj = BeautifulSoup(html)
    title = bs0bj.find('h1').get_text()
    # 抓取title
    content = bs0bj.find('div', {'id': 'mw-content-text'}).find('p').get_text()
    # 抓取content
    store(title, content)
    # 放入数据库
    return bs0bj.find('div', {'id': 'bodyContent'}).findAll('a', href=re.compile('^(/wiki/)((?!:).)*$'))
    # 正则^匹配链接，返回链接的列表
links = getLinks('/wiki/Kevin_Bacon')
try:
    while len(links) > 0:
        newArticle = links[random.randint(0, len(links)-1)].attrs['href']
        # 返回链接
        print(newArticle)
        links = getLinks(newArticle)
        # 循环链接
finally:
    cur.close()
    conn.close()
