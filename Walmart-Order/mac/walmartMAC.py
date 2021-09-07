import csv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from operator import itemgetter
import random
from proxyHandling import *
from driver import *

    
#Function that scrapes walmart page to see if product is cancelled or not
def walmartOrderTracker(rows): 

        #Initializing driver with random proxy/ua
        temp = get_driver()
        driver = temp[0]
        print(f'Proxy: {temp[2]}')
        print(f'User-Agent: {temp[1]}\n')

        #RUNNING PROGRAM ON NORMAL IP

        #options = Options()
        #options.add_argument("--headless")
        #options.add_argument("start-maximized")
        #options.add_experimental_option("excludeSwitches", ["enable-automation"])
        #options.add_experimental_option('useAutomationExtension', False)
        #driver = webdriver.Chrome(r'/Applications/chromedriver', options=options)

        fields = []
        updatedRows = []
        cancels = 0
        success = 0  

        #Getting website and input box elements
        for orders in rows:
            
            #While loop used for rotating proxy/ua if there is px loop.
            pxLoop = True
            while pxLoop:

                #Getting site and input boxes
                driver.get('https://www.walmart.com/account/trackorder')
                emailBox = driver.find_element_by_xpath('//input[@name="email" and @id="email"]')
                numBox = driver.find_element_by_xpath('//input[@name="fullOrderId" and @id="fullOrderId"]')

                #Sending keys with delay email
                email = orders[1]
                for x in range(len(orders[1])):
                    emailBox.send_keys(email[x])
                    time.sleep(random.uniform(0.05, 0.08))
                
                #Sending keys with delay order num
                num = orders[3]
                for x in range(0,13):
                    numBox.send_keys(num[x])
                    time.sleep(random.uniform(0.05, 0.08))

                #Send keys to click enter
                time.sleep(.1)
                numBox.send_keys(Keys.TAB)
                time.sleep(0.6)
                numBox.send_keys(Keys.ENTER)
                time.sleep(.5)

                #Checking for captcha solve
                pxSolving = True
                while pxSolving:
                    #Checking if px is present
                    try:
                        test = driver.find_element_by_xpath('//div[@id="px-captcha"]')
                        time.sleep(.5)
                    #On exception means no of captcha, passes while loop
                    except:
                        pxSolving = False
                        pxLoop = False
                        time.sleep(2)
                    #Caught px, waiting for manual solve
                    else:
                        print('Caught px, waiting to solve...')
                        time.sleep(7)
                        searching = True
                        while searching:
                            try:
                                test = driver.find_element_by_xpath('//p[@style="color: red; margin-top: 4;"]')
                            except:
                                searching = False
                            else:
                                driver.quit()
                                rt = get_driver()
                                print('***Rotating proxy and user-agent***')
                                print(f'New proxy: {rt[2]}')
                                print(f'New user-agent: {rt[1]}')
                                driver = rt[0]
                                pxSolving = False
                                searching = False

                        #In the case of captcha loop, creates new driver, exits pxSolving while loop
                        #Remains in pxLoop while loop
                        





            #Checking to see if item is cancelled
            cancelStatus = driver.find_element_by_xpath('//span[@class="shipping-status-text"]').text
            if cancelStatus == 'Canceled':
                cancels += 1
                updatedRows.append([orders[0], orders[1], orders[2], orders[3], 'FASLE'])
            else:
                success += 1
                updatedRows.append([orders[0], orders[1], orders[2], orders[3], 'TRUE'])

            print(str(len(updatedRows)) + '/' + str(len(rows)) + " Retrieving walmart order status")
        
        driver.quit()
        return updatedRows, cancels, success

#Creates csv file with all the products
def csvCreate(newRows, cancels, success):
    with open('walmartAccounts.csv', 'w', newline='') as file:
        sortedList = sorted(newRows, key=itemgetter(0))
        writer = csv.writer(file)
        writer.writerow(['user', 'email', 'password', 'orderNum', 'success?', '#success= ' + str(success), '#cancels= ' + str(cancels)])
        writer.writerows(sortedList)

