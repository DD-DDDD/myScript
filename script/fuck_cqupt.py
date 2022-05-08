import time
import smtplib
from lxml import etree
from selenium import webdriver
from email.mime.text import MIMEText
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BAD = '解析失败'
GOOD = '解析成功'

def sendEmail(message, add="状态变更通知"):
    # 邮箱地址
    user = "xxxxxx"
    # 授权码
    pwd = "xxxxxx"
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
        print('邮件发送成功')
        return True
    except:
        print('邮件发送失败')
        return False
    finally:
        s.quit()


def get_result(driver):
    try:
        driver.refresh()
        # 切换 frame
        driver.switch_to_frame('topmenuFrame')
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "DataList1_ctl02_hykMenu")))

        driver.find_element_by_id('DataList1_ctl02_hykMenu').click()

        # 切换 frame
        driver.switch_to_default_content()
        driver.switch_to_frame('MenuFrame')
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "tree0_4_a")))

        driver.find_element_by_id('tree0_4_a').click()

        # 切换 frame
        driver.switch_to_default_content()
        driver.switch_to_frame('PageFrame')
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "ctl00_contentParent_dgData")))

        # 查看详情
        driver.find_element_by_id('ctl00_contentParent_dgData_ctl02_hykEdit').click()

        # 切换 frame
        driver.switch_to_default_content()
        driver.switch_to_frame('psEdit')
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tabs")))

        driver.find_element_by_xpath('//div[@class="tabs-wrap"]/ul/li[6]/a').click()
        # 切换 frame
        driver.switch_to_frame('lwpsInfo')
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "ctl00_contentParent_dgData")))

        # 获取表格数据
        soup = etree.HTML(driver.page_source)
        rows = soup.xpath('//*[@id="ctl00_contentParent_dgData"]/tbody/tr')

        first = rows[1].xpath('td/text()')
        first_mark = one[4].strip()
        first_result = one[5].strip()
        second = rows[2].xpath('td/text()')
        second_mark = two[4].strip()
        second_result = two[5].strip()

        print('--' * 20)
        print(f'第一行成绩: {first_mark}')
        print(f'第一行结果: {first_result}')
        print(f'第二行成绩: {second_mark}')
        print(f'第二行结果: {second_result}')

        if first_mark!= '' and first_result != '':
            sendEmail('第一行结果出了!!! 成绩: {}, 结果: {}'.format(first_mark, first_result))
        else:
            print('第一行结果没变')
        if second_mark != '良好' and second_result != '同意答辩':
            sendEmail('第二行结果出了!!! 成绩: {}, 结果: {}'.format(second_mark, second_result))
        else:
            print('第二行结果没变')

        print('--' * 20)
        return GOOD
    except:
        print('解析评审错误')
        sendEmail('程序解析错误，检查', '程序错误')
        return BAD
    finally:
        driver.quit()


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
    # 统一认证码
    un = 'xxxxx'
    # 密码
    pwd = 'xxxxx'

    firefox_path = 'driver/geckodriver.exe'
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    firefox_options.add_argument('--disable-gpu')
    driver = webdriver.Firefox(executable_path=firefox_path, options=firefox_options)

    d = login(un, pwd, driver)

    # 获取学位论文评审结果
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    status_str = get_result(d)
    while True:
        if status_str == BAD:
            # 退出程序
            break
        # 三分刷新一次网页
        time.sleep(3 * 60)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        status_str = get_result(d)
