from selenium import webdriver
<<<<<<< HEAD
from proxyHandling import *
import random
import os

#Create driver
chrome_options = webdriver.ChromeOptions()
def get_driver():
    rt = rotate()
    pluginfile = rt[0]
    ua = rt[1]
    ip = rt[2]
    #New proxy/ua
    chrome_options.add_extension(pluginfile)
    chrome_options.add_argument('--user-agent=%s' % ua)
    #Setting window size
    chrome_options.add_argument("start-maximized")

=======
import os

def get_driver(pluginfile):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_extension(pluginfile)
    chrome_options.add_argument('--user-agent=%s' % True)
    chrome_options.add_argument("start-maximized")
>>>>>>> eae94e90624d1a715520b71ff10918dcabaaed34
    chrome_options.add_argument('no-sandbox')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(
        os.path.join(r'/Users/finnbassill/Downloads', 'chromedriver'),
        chrome_options=chrome_options)

<<<<<<< HEAD
    return driver, ua, ip
=======
    return driver
>>>>>>> eae94e90624d1a715520b71ff10918dcabaaed34
