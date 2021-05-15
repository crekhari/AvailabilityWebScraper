from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import random,pickle,os,time,sys,requests
from bs4 import BeautifulSoup
from re import sub
from decimal import Decimal
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading

class AmazonAutomation():

    def __init__(self):
        #option = webdriver.ChromeOptions()
        #option.add_argument('--disable-infobars')
        self.driver = webdriver.Chrome('/Users/chiraag/chromedriver')#, options=option)

    def tearDown(self):
        self.driver.close()

    def setWebsiteLocation(self, homeLink):  
        self.driver.get(homeLink)
        
    def executeTest(self,file, homeLink, link):
        self.setWebsiteLocation(homeLink)
        #self.checkCookies(file, homeLink, link)
        self.checkAvailability(homeLink, link)
        #self.tearDown()
        
    def placeOrder(self):
        self.driver.find_element_by_xpath("//input[@id='add-to-cart-button']").click()
        self.driver.find_element_by_id("hlb-ptc-btn-native").click()
        #self.driver.find_element_by_xpath("//input[@name='placeYourOrder1']").click() # THIS WILL PLACE THE ORDER -- DO NOT REMOVE UNLESS YOU ARE WILLING TO PURCHASE
        print("Item order has been placed")

    def checkAvailability(self, homeLink, link):
        
        if(link != self.driver.current_url):
            print("it is not equal")
            self.driver.get(link)
        boolean = True
        while(boolean):
            k = random.randint(5, 15)
            passDriver = None
            
            try:
                    price = self.getPrice()
                    if(price > 1900 or price < 1500):
                        print("Reached inside of or statment")
                        print("sleeping now for " + str(k) + " seconds")
                        time.sleep(k)
                        self.driver.refresh()
                    else:
                        self.placeOrder()
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
    

    def addCookies(self, file):
        pickle.dump(self.driver.get_cookies(), open(file,"wb"))

    def loadCookies(self,file, link):
        cookies = pickle.load(open(file, "rb"))
        print("adding cookies then for loop")

        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.get(link)
        print("Cookies should be added")
        
        #self.driver.get(link)

    def checkIfCookiesLoaded(self, file):
        if self.driver.find_element_by_id('nav-link-accountList-nav-line-1').text == "Hello, Chiraag":
            print("cookies loaded properly")
            return True
        else:
            os.remove(file)
            return False


    def checkCookies(self, file, homeLink, link):
        print("starting checkCookies")
        # This try except checks if there is a cookies.pkl file.
        # If there is not, then will create the file, login, and add cookies. 
        # If there is the file, then the method will add the cookies into the web browser
        
        try:
            filesize = os.path.getsize(file)
            print(filesize)
            if filesize == 0:
                print("File is there, but it is empty\nLogging in and then adding cookies")
                self.login(homeLink, link)
                print("login complete")
                self.addCookies(file)
            else:
                print("File exists and is filled with cookies")
        except OSError as e:
            print("File is not there\nFile is being created and cookies are being added to cookies.pkl\nLogging in and then adding cookies")
            self.login(homeLink,link)
            self.addCookies(file)
            self.setWebsiteLocation(link)
            return
        self.loadCookies(file, link)
        if self.checkIfCookiesLoaded(file) == False:
            self.checkCookies(file,homeLink,link)
            print("Cookies file has been deleted and new on is getting added")

    def login(self, homeLink, link):
        loginCredentials = open('loginCredentials.txt', 'r')
        Lines = loginCredentials.readlines()
        signInBtn = self.driver.find_element_by_xpath("//span[@class='nav-line-2 nav-long-width']")
        signInBtn.click()

        username = self.driver.find_element_by_name('email')
        username.send_keys(Lines[0])
       
        self.driver.find_element_by_id('signInSubmit').click()
        
        password = self.driver.find_element_by_id('ap_password')
        password.send_keys(Lines[1])
        
        self.driver.find_element_by_name("rememberMe").click()
        passwordSumbit = self.driver.find_element_by_id('signInSubmit').click()

        time.sleep(3) #DO NOT REMOVE --  This is needed in order for the cookies to load properly

    #https://www.amazon.com/EVGA-GeForce-Technology-Backplate-24G-P5-3987-KR/dp/B08J5F3G18

if __name__ == "__main__":
    file = "amazonCookies.pkl"
    homeLink = 'https://www.amazon.com'
    link = 'https://www.amazon.com/gp/product/B079KYZ9FW?pf_rd_r=4ZYXRC10NATBQ9J26K1P&pf_rd_p=5ae2c7f8-e0c6-4f35-9071-dc3240e894a8&pd_rd_r=39d8b0c5-6ca8-41a8-973c-da08ddc08960&pd_rd_w=dcGK4&pd_rd_wg=cUqPu&ref_=pd_gw_unk'
    taskmaster = AmazonAutomation()
    taskmaster.setWebsiteLocation(homeLink)
    taskmaster.checkCookies(file, homeLink, link)
    taskmaster.tearDown()
    for _ in range(2):
        taskmaster = AmazonAutomation()
        testThread = threading.Thread(target=taskmaster.executeTest, args=(file, homeLink, link))
        testThread.start()
        #taskmaster.executeTest("amazonCookies.pkl", 'https://www.amazon.com', 'https://www.amazon.com/gp/product/B079KYZ9FW?pf_rd_r=4ZYXRC10NATBQ9J26K1P&pf_rd_p=5ae2c7f8-e0c6-4f35-9071-dc3240e894a8&pd_rd_r=39d8b0c5-6ca8-41a8-973c-da08ddc08960&pd_rd_w=dcGK4&pd_rd_wg=cUqPu&ref_=pd_gw_unk')