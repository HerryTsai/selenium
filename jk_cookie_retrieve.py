import time
import re
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup

#cookies登入
def login():
    cookies = dict()
    fpr = open("jk_cookie.txt", "r")
    line = fpr.readline()
    while(line):
        line = line.strip('\n')
        cookies["name"], cookies["value"] = line.split("   ")
        line = fpr.readline()
        Browser.add_cookie({'name': cookies["name"],'value': cookies["value"]})

    fpr.close()
    Browser.get("https://www.jkforum.net/forum.php")

#留言
def leaveMessage(url):
    Browser.get(url)
    Browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    Browser.find_element_by_name('message').send_keys("謝謝大大的分享，這對我很有幫助")
    Browser.find_element_by_name('replysubmit').send_keys(Keys.ENTER)
    time.sleep(2)

#獲取第一頁所有連結
def catchAllUrl(url):
    thePageUrl = set()
    html = urlopen(url)
    bsObj = BeautifulSoup(html.read(), 'lxml')
    for link in bsObj.find("ul", {"id": "waterfall"}).findAll("div", {"class" : "c cl"}):
        url = link.find("a", {"href" : re.compile("^(thread)")})
        thePageUrl.add("https://www.jkforum.net/" + url.attrs["href"])

    return thePageUrl

#下載檔案
def retrieveImg(url, num):
    i = 0
    allImg = Browser.find_elements_by_tag_name('img')
    for img in allImg:
        if re.match('aimg', img.get_attribute('id')):
            try:
                urlretrieve(img.get_attribute('zoomfile'), newFile(num) + '/' + str(i) + img.get_attribute('zoomfile')[-4:])
            except:
                print(str(i) + " doesn't work")
            else:
                i += 1
                time.sleep(10)

#新增資料夾
def newFile(num):
    path = 'D:/' + str(i)
    if not os.path.isdir(path):
        os.mkdir(path)
    return path

opt = webdriver.ChromeOptions()
opt.add_argument('User-Agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"')
Browser = webdriver.Chrome(executable_path=r"D:\chromedriver", chrome_options=opt)
Browser.get('https://www.jkforum.net/forum.php')

login()

allUrl = catchAllUrl('https://www.jkforum.net/forum-640-1.html')
i = 0
for link in allUrl:
    print("cosplay  " + str(i))
    leaveMessage(link)
    retrieveImg(link, i)
    time.sleep(30)
    i += 1

Browser.close()