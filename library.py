import requests
import pytesseract
import time
import datetime
import smtplib
from PIL import Image
from bs4 import BeautifulSoup
from http import cookiejar
from email.mime.text import MIMEText

# 设置时间便于后面的处理和判断
today = str(datetime.date.today())
the_date = datetime.date(int(today.split('-')[0]), int(today.split('-')[1]), int(today.split('-')[2]))
days = datetime.timedelta(days=3)


# 设置headers
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': '202.196.13.8:8080',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
}
# 打开session。
session = requests.Session()
# 保存cookies
session.cookies = cookiejar.LWPCookieJar(filename='cookies')
try:
    # session加载cookies
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")


# 发送邮件
def SendEmail(book_name, add="已借阅"):
    user = "1775718554@qq.com"
    pwd  = "ltfbfvviekvfhihc"
    to   = "1775718554@qq.com"

    msg = MIMEText("{}".format(add))
    msg["Subject"] = " {} 快到期了！".format(book_name)
    msg["From"]    = user
    msg["To"]      = to

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(user, pwd)
        s.sendmail(user, to, msg.as_string())
        s.quit()
        return True
    except:
        return False

# 生成当前时间的时间戳
def timestamp():
    str_datetime = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), "%Y-%m-%d %H:%M:%S.%f")
    time_stamp = int(str_datetime.timetuple())*1000.0 + str_datetime.microsecond / 1000.0
    return time_stamp

# 验证码识别
def get_captcha():
    captcha_url = "http://202.196.13.8:8080/reader/captcha.php"
    x = 0
    bin = session.get(captcha_url, headers=headers).content
    with open("/home/jasd/python/%s.jpg" % x, "wb")as file:
        file.write(bin)
    image = Image.open("/home/jasd/python/0.jpg")
    code = pytesseract.image_to_string(image)
    return code


# 借阅
def renew_book(number, check):
    params_data = {
            'check':check,
            'bar_code': number,
            'captcha': get_captcha,
            'time': timestamp(),
            }
    test = session.get('http://202.196.13.8:8080/reader/ajax_renew.php', headers=headers, data=params_data)
    soup = BeautifulSoup(test.text)
    if soup.find('font', {'color': 'red'}):
        return False
    else:
        return True

# 登录并获取页面信息
def main(xuehao):
    from_data = {
        'number': xuehao,
        'passwd': 'jianaosiding',
        'captcha': get_captcha(),
        'select': 'cert_no',
        'returnurl': '',
        }
    session.post("http://202.196.13.8:8080/reader/redr_verify.php", data=from_data, headers=headers)
    library_info = session.get('http://202.196.13.8:8080/reader/book_lst.php', headers=headers)
    soup = BeautifulSoup(library_info.text, 'lxml')
    name = [name.get_text() for name in soup.findAll('a', {'class': 'blue'})]
    number = [number.get_text for number in soup.findAll('td', {'width': '10%'})]
    time = [time.get_text().split(' ')[0] for time in soup.findAll('font')[1:]]
    end_time = [datetime.date(int(date1.split('-')[0]), int(date1.split('-')[1]), int(date1.split('-')[2])) for date1 in time]
    checks = [check.get('onclick').split("'")[3] for check in soup.findAll('input', {'title': 'renew'})]


    for end in end_time:
        if end - the_date <= days:
            ind = end_time.index(end)
            rank = number[ind]
            check = checks[ind]
            if renew_book(number=rank, check=check):
                SendEmail(name[ind])
            else:
                SendEmail(name[ind], add="未借阅")
    else:
        print('SomeWhat')


if __name__ == '__main__':
    main(str(541510020140))
