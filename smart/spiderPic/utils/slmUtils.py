from selenium import webdriver
import time
import re


def getDriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome('D:\Software\driver\chromedriver.exe', 0, chrome_options)
    return driver


def showBaiduDialog():
    driver = getDriver()
    driver.maximize_window()
    driver.implicitly_wait(6)
    driver.get("https://www.baidu.com")
    time.sleep(1)
    driver.execute_script("window.alert('这是一个alert弹框。');")


def scrollBaidu():
    driver = getDriver()
    driver.get("https://tieba.baidu.com/index.html")
    js = "window.scrollTo(0,document.body.scrollHeight);"  # 拉到最底部
    driver.execute_script(js)
    time.sleep(3)


def executeScript():
    driver = getDriver()
    driver.get('http://qyaqy.lofter.com')
    getScriptInput = """
                        var keywordInput = document.getElementById("control_frame").attributes["src"].value ;
                        return keywordInput ;
                        """
    # scriptInputElement = driver.execute_script(getScriptInput)
    scriptInputElement = driver.execute_script(getScriptInput)
    print(scriptInputElement)


def get_lofter_id(username):
    try:
        url = 'http://%s.lofter.com' % username
        driver = getDriver()
        driver.get(url)
        getScriptInput = """
                                var keywordInput = document.getElementById("control_frame").attributes["src"].value ;
                                return keywordInput ;
                                """
        scriptInputElement = driver.execute_script(getScriptInput)
        id_reg = 'http://www.lofter.com/control\?blogId=(.*)'
        blogid = re.search(id_reg, scriptInputElement).group(1)
        print('The blogid of %s is: %s' % (username, blogid))
        return blogid
    except Exception as e:
        print('get blogid from http://%s.lofter.com failed' % username)
        print('please check your username.')
        exit(1)

# showBaiduDialog()
# scrollBaidu()
# executeScript()
# print(getBlogId("qyaqy"))
