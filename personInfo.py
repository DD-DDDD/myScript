import requests
import ast
import time 
from threading import Thread
from queue import Queue
from pymongo import MongoClient


def run_time(func):
    def wrapper(*args, **kw):
        start = time.time()
        func(*args, **kw)
        end = time.time()
        print("running", end-start, "s")
    return wrapper


class GetPersonInfo(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ko-KR;q=0.6,ko;q=0.5,ja-JP;q=0.4,ja;q=0.3',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': '',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
        }
        self.data = {
           # xuehao
        }

        self.qid = Queue()
        self.thread_num = 8
        client = MongoClient(host='localhost', port=27017)
        db = client['Info']
        self.col = db['PersonInfo']
        self.infourl = "http://xxx.xxx.edu.cn/dxxxxxx/student/xxxxx/paisanStu"

    def genUrl(self):
        for i, j in self.data.items():
            print("Geting {}!".format(i))
            number = j
            # 541810020140
            # 540910020140
            # 000100000000
            baseId = int(number[0:2]+"09"+number[4:10]+"01")
            baseList = [k for k in range(baseId, baseId+1000000000, 100000000)]
            gradList = [ self.qid.put(n) for m in baseList for n in range(m, m+60)]


    def getInfo(self):
        while not self.qid.empty():
            ids = self.qid.get()

            data = {
                'stu_id': str(ids)
            }
            rep = requests.post(self.infourl, headers=self.headers, data=data).text
            try:
                repDict = ast.literal_eval(rep)
                # print(repDict)
                self.col.insert_one(repDict)
                print("GET {}!".format(ids))
            except:
                pass
    
    @run_time
    def run(self):
        self.genUrl()

        ths = []
        for _ in range(self.thread_num):
            th = Thread(target=self.getInfo)
            th.start()
            ths.append(th)
        for th in ths:
            th.join()


if __name__ == "__main__":
    info = GetPersonInfo()
    info.run()

