from selenium.webdriver.chrome import options
from seleniumwire import webdriver
import csv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from operator import itemgetter
import random
from proxyHandling import *

    
#Function that scrapes walmart page to see if product is cancelled or not
def walmartOrderTracker(rows): 

    #Calling proxy handling function
    #ph = proxyHandling()
    #Optional Proxy 
    #options = {
    #'proxy': {
    #    'http': f'{ph[0][0]}',
    #    'https': f'{ph[1][0]}',
    #    'no_proxy': 'localhost,127.0.0.1'
    #}}
    #options.add_argument("start-maximized")
    #options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #options.add_experimental_option('useAutomationExtension', False)
    #driver = webdriver.Chrome(r'/Applications/chromedriver', seleniumwire_options=options)

    options = Options()
    #options.add_argument("--headless")
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(r'/Applications/chromedriver', options=options)

    fields = []
    updatedRows = []
    cancels = 0
    success = 0  

    #Getting website and input box elements
    for orders in rows:
        driver.get('https://www.walmart.com/account/trackorder')
        emailBox = driver.find_element_by_xpath('//input[@name="email" and @id="email"]')
        numBox = driver.find_element_by_xpath('//input[@name="fullOrderId" and @id="fullOrderId"]')

        #Sending keys with delay email
        email = orders[1]
        for x in range(len(orders[1])):
            emailBox.send_keys(email[x])
            time.sleep(random.uniform(0.04, 0.12))
        
        #Sending keys with delay order num
        num = orders[3]
        for x in range(0,13):
            numBox.send_keys(num[x])
            time.sleep(random.uniform(0.04, 0.12))

        #Send keys to click enter
        time.sleep(.1)
        numBox.send_keys(Keys.TAB)
        time.sleep(0.5)
        numBox.send_keys(Keys.ENTER)
        time.sleep(.7)

        #Checking for captcha solve
        captchaSolving = True
        while captchaSolving:
            try:
                test = driver.find_element_by_xpath('//div[@id="px-captcha"]')
                time.sleep(.5)
            except:
                captchaSolving = False
                time.sleep(2)
            else:
                print('Caught captcha, waiting to solve...')
                time.sleep(6)

        #Checking to see if item is cancelled
        cancelStatus = driver.find_element_by_xpath('//span[@class="shipping-status-text"]').text
        if cancelStatus == 'Canceled':
            cancels += 1
            updatedRows.append([orders[0], orders[1], orders[2], orders[3], 'FASLE'])
        else:
            success += 1
            updatedRows.append([orders[0], orders[1], orders[2], orders[3], 'TRUE'])

        print(str(len(updatedRows)) + '/' + str(len(rows)) + " retrieving walmart order status")
    
    driver.quit()
    return updatedRows, cancels, success

#Creates csv file with all the products
def csvCreate(newRows, cancels, success):
    with open('walmartAccounts.csv', 'w', newline='') as file:
        sortedList = sorted(newRows, key=itemgetter(0))
        writer = csv.writer(file)
        writer.writerow(['user', 'email', 'password', 'orderNum', 'success?', '#success= ' + str(success), '#cancels= ' + str(cancels)])
        writer.writerows(sortedList)

