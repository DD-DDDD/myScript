# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:46:31 2016

@author: ricaito
"""

import requests as rq
import json
import time 
import pandas as pd

keyword = input("please enter a job keyword:")#输入职位关键词
lagou_url = "http://www.lagou.com/jobs/positionAjax.json?first=false&pn={0}&kd={1}"
lagou_python_data = []

for i in range(1,31):
    print("crawling{0}".format(i))
    lagouurl = lagou_url.format(i,keyword)
    lagou_data = json.loads(rq.get(lagouurl).text)#请求网址，返回json
    time.sleep(2)#暂停2秒
    lagou_python_data.extend(lagou_data['content']['positionResult']['result'])
    

position_data = pd.DataFrame(lagou_python_data)
position_data.to_csv("C:/Users/ricaito/Desktop/test/./{0}_job.csv".format(keyword),index = False)
#保存数据位csv格式在电脑目录下
print("Download Done!")

