from selenium import webdriver
import os

def get_driver(pluginfile):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_extension(pluginfile)
    chrome_options.add_argument('--user-agent=%s' % True)
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('no-sandbox')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(
        os.path.join(r'/Users/finnbassill/Downloads', 'chromedriver'),
        chrome_options=chrome_options)

    return driver