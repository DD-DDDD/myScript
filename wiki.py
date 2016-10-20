import re
import random
from bs4 import BeautifulSoup
from urllib.request import urlopen
import datetime
import json
random.seed(datetime.datetime.now())


def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bs0bj = BeautifulSoup(html, "lxml")
    rex = '^(/wiki/)((?!:).)*$'
    #
    return bs0bj.find("div",
                      {'id': 'bodyContent'}).findAll('a', href=re.compile(rex))


def getHistoryIPs(pagesUrl):
    pagesUrl = pagesUrl.replace('/wiki/', '')
    # 编辑历史页面url连接的格式
    historyUrl = ("http://en.wikipedia.org/w/index.php?title=" +
                  pagesUrl + "&action=history")
    print("history url is "+historyUrl)
    html = urlopen(historyUrl)
    bs0bj = BeautifulSoup(html, "lxml")
    ipAddresses = bs0bj.findAll('a', {'class': 'mw-anonuserlink'})
    addressList = set()
    for ipAddress in ipAddresses:
        addressList.add(ipAddress.get_text())
    return addressList


def getCountry(ipAddres):
    try:
        response = urlopen("http://freegeoip.net/json/" +
                           ipAddres).read().decode('utf-8')
    except HTTPError:
        return None
    responseJson = json.loads(response)
    return responseJson.get('country_code')

links = getLinks('/wiki/Python_(programming_language)')

while (len(links) > 0):
    for link in links:
        print("-----------------")
        historyIPs = getHistoryIPs(link.attrs['href'])
        for historyIP in historyIPs:
            country = getCountry(historyIP)
            if country is not None:
                print(historyIP+"is from "+country)

    newLink = links[random.randint(0, len(liks)-1)].attrs['href']
    links = getLinks(newLink)
