import requests
import re
import urllib

keyword = input("keyword:")
key = urllib.parse.quote(keyword)
payload = {
    'callCount': '1',
    'scriptSessionId': '${scriptSessionId}190',
    'httpSessionId': 'f090ee8789f5413792d5b5eed4568e82',
    'c0-scriptName': 'OpenSearchBean',
    'c0-methodName': 'searchVideo',
    'c0-id': '0',
    'c0-param0': 'string:{0}'.format(key),
    'c0-param1': 'number:1',
    'c0-param2': 'number:100',
    'batchId': '1478666899720'
    }
data = requests.post("http://c.open.163.com/dwr/call/plaincall/OpenSearchBean.searchVideo.dwr", data=payload).text
reg = re.compile("http://open.163.com.*?\.html")
links = re.findall(reg, data)
for link in links:
    print(link)
