import smtplib
import time
from email.mime.text import MIMEText

from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# 发送邮件
def sendEmail(message, add="状态变更通知"):
    # 邮箱地址
    user = "xxxxxx"
    # 授权码
    pwd = "xxxxx"
    # 邮箱地址
    to = "xxxxxxx"

    msg = MIMEText("{}".format(add))
    msg["Subject"] = message
    msg["From"] = user
    msg["To"] = to

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(user, pwd)
        s.sendmail(user, to, msg.as_string())
        s.quit()
        print('邮件发送成功')
        return True
    except:
        print('邮件发送失败')
        return False


def get_result(driver):
    try:
        driver.refresh()
        driver.switch_to_frame('topmenuFrame')
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "DataList1_ctl02_hykMenu")))

        driver.find_element_by_id('DataList1_ctl02_hykMenu').click()

        driver.switch_to_default_content()
        driver.switch_to_frame('MenuFrame')
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "tree0_4_a")))

        driver.find_element_by_id('tree0_4_a').click()

        driver.switch_to_default_content()
        driver.switch_to_frame('PageFrame')
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "ctl00_contentParent_dgData")))

        # 查看详情
        driver.find_element_by_id('ctl00_contentParent_dgData_ctl02_hykEdit').click()

        driver.switch_to_default_content()
        driver.switch_to_frame('psEdit')
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tabs")))

        driver.find_element_by_xpath('//div[@class="tabs-wrap"]/ul/li[6]/a').click()
        driver.switch_to_frame('lwpsInfo')
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "ctl00_contentParent_dgData")))

        soup = etree.HTML(driver.page_source)
        rows = soup.xpath('//*[@id="ctl00_contentParent_dgData"]/tbody/tr')
        one = rows[1].xpath('td/text()')
        one_mark = one[4].strip()
        one_result = one[5].strip()
        two = rows[2].xpath('td/text()')
        two_mark = two[4].strip()
        two_result = two[5].strip()

        print('--' * 20)
        print(f'第一行成绩: {one_mark}')
        print(f'第一行结果: {one_result}')
        print(f'第二行成绩: {two_mark}')
        print(f'第二行结果: {two_result}')

        if one_mark != '' and one_result != '':
            sendEmail('第一行结果出了!!!\n成绩: {}, 结果: {}'.format(one_mark, one_result))
        else:
            print('第一行结果没变')
        if two_mark != '良好' and two_result != '同意答辩':
            sendEmail('第二行结果出了!!!\n成绩: {}, 结果: {}'.format(two_mark, two_result))
        else:
            print('第二行结果没变')

        print('--' * 20)
        return '解析正确'
    except:
        print('解析评审错误')
        # 程序错误发送邮件通知
        sendEmail('程序解析错误，检查', '程序错误')
        return '解析错误'


def login(username, password, dr):
    url = 'https://ids.cqupt.edu.cn/authserver/login?service=http%3a%2f%2fgs.cqupt.edu.cn%2fCaslogin.aspx'
    dr.get(url)
    # 设置用户名
    try:
        dr.find_element_by_id('username').send_keys(username)
        # 设置密码
        dr.find_element_by_id('password').send_keys(password)
        # 设置记录
        dr.find_element_by_id('rememberMe').send_keys('true')
        print('登录...')
    except:
        print('登录错误')

    # click
    dr.find_element_by_id('login_submit').click()

    return dr


if __name__ == '__main__':
    un = 'xxxxx'
    pwd = 'xxxxx'

    firefox_path = 'driver/geckodriver.exe'
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    firefox_options.add_argument('--disable-gpu')
    driver = webdriver.Firefox(executable_path=firefox_path, options=firefox_options)
    # driver = webdriver.Firefox(executable_path=firefox_path)

    d = login(un, pwd, driver)

    # 获取学位论文评审结果
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    status_str = get_result(d)
    if status_str == '解析错误':
        d.quit()
        exit(0)
    while True:
        time.sleep(3 * 60)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        status_str = get_result(d)
        if status_str == '解析错误':
            d.quit()
            exit(0)
