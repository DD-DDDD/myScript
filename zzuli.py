import requests
from bs4 import BeautifulSoup
import re
import urllib.request
loginurl = 'http://my.zzuli.edu.cn/userPasswordValidate.portal'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Cookie': 'Hm_lvt_1e7bb0586b7e61911a64e086492a7916=1477624531; Hm_lpvt_1e7bb0586b7e61911a64e086492a7916=1477624531; _ga=GA1.3.297408136.1477624531; _gat=1; JSESSIONID=00009jL4YpBHimeCREM4FNAcem5:164h0btfq',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}
data = {
    'Login.Token1': 'xuehao',
    'Login.Token2': 'password',
    'goto': 'http://my.zzuli.edu.cn/loginSuccess.portal',
    'gotoOnFail': 'http://my.zzuli.edu.cn/loginFailure.portal'
}
s = requests.Session()
s.post(loginurl, data=data, headers=headers, verify=False)
html = s.get('http://my.zzuli.edu.cn/index.portal?.pn=p461_p462')
soup = BeautifulSoup(html.text, "lxml")

print(soup)
