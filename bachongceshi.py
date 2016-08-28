
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError


def gettitle(url):
    try:
        wed_data = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsobj = BeautifulSoup(wed_data,"lxml")
        title = bsobj.body.h1
    except AttributeError as e :
        return None
    return title
title = gettitle ("https://www.douban.com/")
if title ==None:
    print("title could not be found")
else:
    print(title)







