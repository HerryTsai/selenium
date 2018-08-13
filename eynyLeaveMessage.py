import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

#登入頁面
def login():
    LoginUrl= ('http://www.eyny.com/member.php?mod=logging&action=login')
    UseName = ('******')
    UsePass = ('******')

    Browser.get(LoginUrl)
    Browser.find_element_by_name('username').send_keys(UseName)
    Browser.find_element_by_name('password').send_keys(UsePass)
    Browser.find_element_by_name('loginsubmit').send_keys(Keys.ENTER)

#進行留言
def leaveMessage(url):
    Browser.get(url)
    Browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    Browser.find_element_by_name('message').send_keys("謝謝大大的分享，這對我很有幫助")
    Browser.find_element_by_name('replysubmit').send_keys(Keys.ENTER)
    time.sleep(2)

#爬取第一頁所有的連結
def catchAllUrl():
    thePageUrl = set()
    LoginUrl= ('http://www.eyny.com/forum-56-1.html')
    html = urlopen(LoginUrl)
    bsObj = BeautifulSoup(html.read(), 'lxml')
    for link in bsObj.findAll("tbody", id = re.compile("^(normalthread)(_)([0-9]*$)")):
        url = link.find("a", {"href" : re.compile("^(thread)")})
        thePageUrl.add("http://www.eyny.com/" + url.attrs["href"])

    return thePageUrl

i = 0
allUrl = catchAllUrl()
Browser = webdriver.Chrome(executable_path=r"D:\chromedriver")
login()
for link in allUrl:
    leaveMessage(link)
    time.sleep(45)
    print(i)
    i += 1
Browser.close()