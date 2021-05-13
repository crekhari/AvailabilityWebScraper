from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import random,pickle,os,time,sys,requests


class AmazonAutomation():

    def __init__(self):
        self.driver = webdriver.Chrome('/Users/chiraag/chromedriver')

    def tearDown(self):
        self.driver.close()

    def setWebsiteLocation(self, homeLink):
        self.driver.get(homeLink)
        
    def executeTest(self,file, homeLink, link):
        i=1
        self.setWebsiteLocation(homeLink)
        #self.login(homeLink, link)
        self.checkCookies(file, homeLink, link)
        # add to cart()

    def addCookies(self, file):
        pickle.dump(self.driver.get_cookies(), open(file,"wb"))

    def loadCookies(self,file, link):
        cookies = pickle.load(open(file, "rb"))
        print("adding cookies then for loop")
        
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        print("Cookies should be added")
        
        self.driver.get(link)

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
        self.loadCookies(file, link)

        #cookieFile = open('cookies.txt', 'a')
        #figure out cookies or just use beatiful soup but cookies will be easier and faster if you figure this out
        #cookies = {}
        #cookies = self.driver.get_cookies()
        #for cookie in cookies:
         #   if(cookies[cookie] == "www.amazon.com"):
          #      print("FOUND IT")
        #self.driver.add_cookie({"name": "foo", "value": "bar"})
        #print(self.driver.get_cookie("foo"))
    
    def checkLogin(self, homeLink, link):
        i=1



    def login(self, homeLink, link):
        signInBtn = self.driver.find_element_by_xpath("//span[@class='nav-line-2 nav-long-width']")
        signInBtn.click()

        username = self.driver.find_element_by_name('email')
        username.send_keys("crekhari@gmail.com")
        usernameSubmit = self.driver.find_element_by_id('continue').click()

        password = self.driver.find_element_by_id('ap_password')
        password.send_keys("Drlal12#")
        passwordSumbit = self.driver.find_element_by_id('signInSubmit').click()

        time.sleep(3)

    

    

if __name__ == "__main__":
    taskmaster = AmazonAutomation()
    taskmaster.executeTest("amazonCookies.pkl", 'https://www.amazon.com', 'https://www.amazon.com/EVGA-GeForce-Technology-Backplate-24G-P5-3987-KR/dp/B08J5F3G18')