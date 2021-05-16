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

    def __init__(self, headless, pickleFile, homeLink, link, upperBound, lowerBound):

        if headless == True:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            self.driver = webdriver.Chrome('/Users/chiraag/chromedriver', options=options)
        if headless == False:
            self.driver = webdriver.Chrome('/Users/chiraag/chromedriver')
    
        self.file = pickleFile
        self.homeLink = homeLink
        self.link = link
        self.upperBound = upperBound
        self.lowerBound = lowerBound
        #print(pickleFile + homeLink + link + str(upperBound) + str(lowerBound) + '\n')

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
    botNavigator = open('botNavigator.txt', 'r')
    Lines = botNavigator.readlines()
    botNavigator.close()

    numThreads = int(Lines[0])
    pickleFile = Lines[1]
    homeLink = Lines[2]

    taskmaster = AmazonAutomation(True, pickleFile, homeLink, Lines[3], Lines[4], Lines[5]) #This is to check if the cookies file has the correct or expired cookies
    taskmaster.setWebsiteLocation()
    taskmaster.checkCookies()
    taskmaster.tearDown()
    Lines.pop(0)
    Lines.pop(0)
    Lines.pop(0)

    
    for _ in range(numThreads):
        for x in range(0, len(Lines), 3):
            link = Lines[x]
            upperBound = int(Lines[x+1])
            lowerBound = int(Lines[x+2])
            #print("link is: " + link + " upperBound is: " + str(upperBound) + " lowerBound is: " + str(lowerBound) + '\n')
            taskmaster = AmazonAutomation(True, pickleFile, homeLink, link, upperBound, lowerBound)
            driverThread = threading.Thread(target=taskmaster.executeTest, args=())
            driverThread.start()
        print("Headless Thread created\n")
    '''
    for _ in range(1):
        for x in range(0, len(Lines), 3):
            link = Lines[x]
            upperBound = int(Lines[x+1])
            lowerBound = int(Lines[x+2])
            #print("link is: " + link + " upperBound is: " + str(upperBound) + " lowerBound is: " + str(lowerBound) + '\n')
            taskmaster = AmazonAutomation(False, pickleFile, homeLink, link, upperBound, lowerBound)
            driverThread = threading.Thread(target=taskmaster.executeTest, args=())
            driverThread.start()
        print("Debuggin Head Thread created\n")
    '''
    