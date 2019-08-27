from apscheduler.schedulers.background import BackgroundScheduler
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse

from RpaMail import mail_msg
from RpaTelegram import telegram_msg
from RpaTwilio import text_msg

from RpaLogging import KTingLog

import requests
import sys


# %% function


def closeAlert(driver):
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass

def currentSitename(url):
    parts = urlparse(url)
    return parts.netloc

def textBackup(driver, txt):
    target_backup = driver.find_element_by_css_selector('textarea')
    target_backup.send_keys(Keys.CONTROL+'a')
    target_backup.send_keys(txt)
    driver.find_element_by_css_selector('input[type=submit]').click()
    
    

def navigateByLink(url, sender, method):
    
    def check(url):
        if not url:
            return False
        if url in visit:
            return False
        if url in q:
            return False
        if url[-1] == '#':
            return False
        return True
    
    sitename = currentSitename(url)
    
    if method == 'XSS':
        test = "<script>alert('XSS testing')</script>"
    
    while True:
        headless = 'n'
        if headless == 'y':
            Options = webdriver.ChromeOptions()
            Options.add_argument('headless')
            Options.add_argument('window-size=1920x1080')
            Options.add_argument("disable-gpu")
            Options.add_argument(
                "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
            driver = webdriver.Chrome('C:/Users/user/Documents/wetube/src/chromedriver.exe', options=Options)
            break
        elif headless == 'n':
            driver = webdriver.Chrome(
                'C:/Users/user/Documents/wetube/src/chromedriver.exe')
            break

    visit = set()
    q = []

    q.append(('base', url))

    driver.implicitly_wait(1)

    while q:
        pg = q.pop(0)
        try:
            url = pg[1].get_attribute('href')
        except:
            url = pg[1]
        if url not in visit:
            if 'http' not in url: continue
            visit.add(url)
            driver.get(url)
            closeAlert(driver)
            
            curl = driver.current_url
            if url != curl and curl in visit : continue
            visit.add(curl)
            
            KTingLogger.info("Visit {curl}".format(curl = curl))

            if sitename != currentSitename(curl):
                KTingLogger.info("Out of Web from {curl}".format(curl = curl))
                print("Out of Web from {curl}".format(curl = curl))
                continue
            
            if method == 'XSS':
                form = driver.find_elements_by_css_selector('form')
                for form2 in form:
                    target = []
                    target += form2.find_elements_by_css_selector('input[type=text]')
                    target += form2.find_elements_by_css_selector('textarea')
                    for textbox in target:
                        backup_text = textbox.text
                        textbox.send_keys(Keys.CONTROL + 'a')
                        textbox.send_keys(test)
                    submit = form2.find_element_by_css_selector(
                        'input[type=submit]')
                    if submit.get_attribute('value') != 'delete':
                        submit.click()
                        try:
                            alert = driver.switch_to.alert
                            alert.accept()
                            err_msg = 'detecting XSS\nAt {current_url}'.format(current_url=curl)
                            sender.msg(err_msg)
                            KTingLogger.info(err_msg)
                            print(err_msg)
                            driver.back()
                            textBackup(backup_text)
                        except:
                            pass
                statusCode = requests.get(driver.current_url).status_code
                if 4 <= statusCode // 100 <=5 :
                    err_msg = 'status code: {statusCode}\nAt Link Name: {name}\nUrl: {current_url}'.format(statusCode = statusCode, name = pg[0], current_url = curl)
                    sender.msg(err_msg)
                    KTingLogger.info(err_msg)
                    print(err_msg)
                    driver.back()
            elif method == 'SQL injection' or method == 'SQL':
                if '?' in curl:
                    try:
                        requests.get(curl+';select *')
                    except:
                        err_msg = 'SQL Injection \nAt Url: {current_url}'.format(current_url = curl)
                        sender.msg(err_msg)
                        KTingLogger.info(err_msg)
                        print(err_msg)
            
            for a in driver.find_elements_by_xpath('.//a'):
                url = a.get_attribute('href')
                if url.split(':')[0] == 'javascript':
                    pg.click()
                elif check(url):
                    q.append((a.text, url))
        
# %% 알림 방식 설정


try:
    how = sys.argv[2]
    contact = sys.argv[3]
    tm = 'TT'
    if how == 'Telegram':
        sender = telegram_msg(int(contact))
    elif how == 'Text Message':
        sender = text_msg(contact)
    elif how == 'Email':
        sender = mail_msg(contact)
except:
    print('error')

# %% Log 설정
    

user_id = sys.argv[5]
KTingLogger = KTingLog(user_id)

# %% Main


url = sys.argv[1]
method = sys.argv[4]

KTingLogger.info('Navigation start')
navigateByLink(url, sender, method)
KTingLogger.info('Navigation end')
