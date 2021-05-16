from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import random,pickle,os,time,sys,requests
from bs4 import BeautifulSoup
from re import sub
from decimal import Decimal
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading

class AmazonAutomation():

    def __init__(self, headless, item):
        botNavigator = open('botNavigator.txt', 'r')
        Lines = botNavigator.readlines()
        botNavigator.close()

        if headless == True:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            self.driver = webdriver.Chrome('/Users/chiraag/chromedriver', options=options)
        if headless == False:
            self.driver = webdriver.Chrome('/Users/chiraag/chromedriver')
    
        if item == "3090":
            self.lowerBound = 1500
            self.upperBound = 2000
            self.file = Lines[0]
            self.homeLink = Lines[1]
            self.link = Lines[2]
    
        if item == "3080a":
            self.lowerBound = 700
            self.upperBound = 1300
            self.file = Lines[0]
            self.homeLink = Lines[1]
            self.link = Lines[3]

        if item == "PS4":
            self.lowerBound = 340
            self.upperBound = 420
            self.file = Lines[0]
            self.homeLink = Lines[1]
            self.link = Lines[4]

        if item == "3080e":
            self.lowerBound = 700
            self.upperBound = 1300
            self.file = Lines[0]
            self.homeLink = Lines[1]
            self.link = Lines[5]
        
        if item == "":
            self.lowerBound = 1000
            self.upperBound = 1500
            self.file = Lines[0]
            self.homeLink = Lines[1]
            #self.link = "https://www.amazon.com/gp/product/B08Z7DXHP5/ref=ox_sc_act_title_1?smid=A3TY2V73IP9GIS&psc=1"

    def tearDown(self):
        self.driver.close()

    def setWebsiteLocation(self):  
        self.driver.get(self.homeLink)
        
    def executeTest(self):
        self.setWebsiteLocation()
        self.loadCookies()
        self.checkAvailability()
        self.tearDown()
        
    def placeOrder(self):
        print("Placing order")
        waiting = WebDriverWait(self.driver,10)
        button = None
        #(submitBtnClick.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[4]")))).click()

        #self.driver.find_element_by_xpath("//input[@id='add-to-cart-button']").click()
        #self.driver.find_element_by_xpath("//input[@aria-labelledby='attachSiNoCoverage-announce']").click()
        #self.driver.find_element_by_xpath("//a[@id='hlb-ptc-btn-native']").click()
        #self.driver.find_element_by_xpath("//input[@name='placeYourOrder1']").click() #THIS WILL PLACE THE ORDER -- DO NOT REMOVE UNLESS YOU ARE WILLING TO PURCHASE
        try:
            addToCart = (waiting.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='add-to-cart-button']")))).click()

            noThanks = (waiting.until(EC.element_to_be_clickable((By.XPATH, "//input[@aria-labelledby='attachSiNoCoverage-announce']"))))
            button = noThanks
            noThanks.click()
            
            self.driver.get("https://www.amazon.com/gp/cart/view.html?ref_=nav_cart")
            checkoutButton = (waiting.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='proceedToRetailCheckout']"))))
            button = checkoutButton
            checkoutButton.click()
            
            placeOrder = (waiting.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='placeYourOrder1']"))))#THIS WILL PLACE THE ORDER -- DO NOT REMOVE UNLESS YOU ARE WILLING TO PURCHASE
            button = placeOrder
            placeOrder.click()
        
        except NoSuchElementException:
            try:
                itemFound = open('itemFound.txt', 'a')
                itemFound.write("Could not find" + button.text + '\n')
                itemFound.close()
            except Exception as e:
                itemFound = open('itemFound.txt', 'a')
                itemFound.write("Something went wrong in NoSuchElementException" + e + '\n')
                itemFound.close()
        except TimeoutException:
            itemFound = open('itemFound.txt', 'a')
            itemFound.write("waited and nothing came back\n")
            itemFound.close()
        except Exception as e:
            itemFound = open('itemFound.txt', 'a')
            itemFound.write(e + '\n')
            itemFound.close()

    def checkAvailability(self):
        boolean = True

        if(self.link != self.driver.current_url):
            print("it is not equal")
            self.driver.get(self.link)
        
        while(boolean):
            k = random.randint(5, 15)            
            try:
                    price = self.getPrice()
                    itemFound = open('itemFound.txt', 'a')
                    itemFound.write(str(price) + '\n')
                    itemFound.close()
                    if(price > self.upperBound or price < self.lowerBound):
                        print("sleeping now for " + str(k) + " seconds")
                        time.sleep(k)
                        self.driver.refresh()
                    else:
                        self.placeOrder()
                        itemFound = open('itemFound.txt', 'a')
                        itemFound.write("Order has been placed\n")
                        itemFound.close()
                        boolean = False
            except Exception:
                print("Could not find price")
                print("sleeping exception for " + str(k) + " seconds")
                time.sleep(k)
                self.driver.refresh()

    def getPrice(self):
        price = self.driver.find_element_by_id("priceblock_ourprice").text
        intPrice = Decimal(sub(r'[^\d.]', '', price))
        print(intPrice)
        return intPrice
    
    def addCookies(self):
        pickle.dump(self.driver.get_cookies(), open(self.file,"wb"))

    def loadCookies(self):
        cookies = pickle.load(open(self.file, "rb"))
        print("adding cookies then for loop")

        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.get(self.link)
        print("Cookies should be added")

    def checkIfCookiesLoaded(self):
        if(self.homeLink != self.driver.current_url):
            print("it is not equal in checkCookiesLoaded")
            self.driver.get(self.homeLink)
        if self.driver.find_element_by_id('nav-link-accountList-nav-line-1').text == "Hello, Chiraag":
            print("cookies loaded properly")
            return True
        else:
            os.remove(self.file)
            return False


    def checkCookies(self):
        # This try except checks if there is a cookies.pkl file.
        # If there is not, then will create the file, login, and add cookies. 
        # If there is the file, then the method will add the cookies into the web browser

        print("starting checkCookies")
        
        try:
            filesize = os.path.getsize(self.file)
            print(filesize)
            if filesize == 0:
                print("File is there, but it is empty\nLogging in and then adding cookies")
                self.login()
                print("login complete")
                self.addCookies()
            else:
                print("File exists and is filled with cookies")
        except OSError as e:
            print("File is not there\nFile is being created and cookies are being added to cookies.pkl\nLogging in and then adding cookies")
            self.login()
            self.addCookies()
            self.setWebsiteLocation()
            return
        self.loadCookies()
        if self.checkIfCookiesLoaded() == False:
            print("Cookies file has been deleted and new on is getting added")
            self.checkCookies()

    def login(self):
        if(self.homeLink != self.driver.current_url):
            print("it is not equal")
            self.driver.get(self.homeLink)
        loginCredentials = open('loginCredentials.txt', 'r')
        Lines = loginCredentials.readlines()
        loginCredentials.close()
        wait = WebDriverWait(self.driver,10)

        (wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@id='nav-link-accountList-nav-line-1']")))).click()
        (wait.until(EC.element_to_be_clickable((By.NAME, 'email')))).send_keys(Lines[0])
        (wait.until(EC.element_to_be_clickable((By.ID, 'signInSubmit')))).click()
        (wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='rememberMe']")))).click()
        (wait.until(EC.element_to_be_clickable((By.ID, 'ap_password')))).send_keys(Lines[1])
        

        time.sleep(3) #DO NOT REMOVE --  This is needed in order for the cookies to load properly
        print("done")

    #https://www.amazon.com/EVGA-GeForce-Technology-Backplate-24G-P5-3987-KR/dp/B08J5F3G18
    #https://www.amazon.com/gp/product/B079KYZ9FW?pf_rd_r=4ZYXRC10NATBQ9J26K1P&pf_rd_p=5ae2c7f8-e0c6-4f35-9071-dc3240e894a8&pd_rd_r=39d8b0c5-6ca8-41a8-973c-da08ddc08960&pd_rd_w=dcGK4&pd_rd_wg=cUqPu&ref_=pd_gw_unk

if __name__ == "__main__":
    
    taskmaster = AmazonAutomation(True, "3090")
    taskmaster.setWebsiteLocation()
    taskmaster.checkCookies()
    taskmaster.tearDown()
    '''
    taskmaster = AmazonAutomation(False, "")
    testThread = threading.Thread(target=taskmaster.executeTest, args=())
    testThread.start()
    '''
    #3090
    for _ in range(2):
        taskmaster = AmazonAutomation(True, "3090")
        testThread = threading.Thread(target=taskmaster.executeTest, args=())
        testThread.start()
    taskmaster = AmazonAutomation(False, "3090")
    testThread = threading.Thread(target=taskmaster.executeTest, args=())
    testThread.start()

    #3080 asus
    for _ in range(2):
        taskmaster = AmazonAutomation(True, "3080a")
        testThread = threading.Thread(target=taskmaster.executeTest, args=())
        testThread.start()
    taskmaster = AmazonAutomation(False, "3080a")
    testThread = threading.Thread(target=taskmaster.executeTest, args=())
    testThread.start()

    #3080 evga
    for _ in range(2):
        taskmaster = AmazonAutomation(True, "3080e")
        testThread = threading.Thread(target=taskmaster.executeTest, args=())
        testThread.start()
    taskmaster = AmazonAutomation(False, "3080e")
    testThread = threading.Thread(target=taskmaster.executeTest, args=())
    testThread.start()
    