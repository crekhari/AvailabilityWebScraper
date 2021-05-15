from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import random,pickle,os,time,sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BestBuyAutomation():

    def __init__(self):
        self.driver = webdriver.Chrome('/Users/chiraag/chromedriver')

    def setWebsiteLocation(self, link):
        self.driver.get(link)

    def executeTest(self, file, link):
        self.setWebsiteLocation(link)
        self.checkCookies(file, link)
        self.registerForQueue()
        self.addToCart()

    def addCookies(self, file):
        pickle.dump(self.driver.get_cookies(), open(file,"wb"))

    def loadCookies(self,file, link):
        cookies = pickle.load(open(file, "rb"))
        print("adding cookies then for loop")
        
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        print("Cookies should be added")
        
        self.driver.get(link)

    def checkCookies(self, file, link):
        print("starting pickle testing")
        # This try except checks if there is a cookies.pkl file.
        # If there is not, then will create the file, login, and add cookies. 
        # If there is the file, then the method will add the cookies into the web browser
        try:
            filesize = os.path.getsize(file)
            print(filesize)
            if filesize == 0:
                print("File is there, but it is empty\nLogging in and then adding cookies")
                self.login()
                print("login complete")
                self.addCookies(file)
            else:
                print("File exists and is filled with cookies")
        except OSError as e:
            print("File is not there\nFile is being created and cookies are being added to cookies.pkl\nLogging in and then adding cookies")
            self.login()
            self.addCookies(file)
        self.loadCookies(file, link)
        

    def login(self):
        print("Sleeping for 10")
        loginCredentials = open('loginCredentials.txt', 'r')
        Lines = loginCredentials.readlines()
        loginCredentials.close()
        dropdownClick = WebDriverWait(self.driver,15)
        dropdownClick = (dropdownClick.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn-unstyled plButton account-button']//*[local-name()='svg']")))).click()
        # time.sleep(10)
        # dropdown = self.driver.find_element_by_xpath("//button[@class='btn-unstyled plButton account-button']//*[local-name()='svg']")
        # dropdown.click()
        signInClick = WebDriverWait(self.driver,20)
        signInClick = (signInClick.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Sign In')))).click()
        # time.sleep(15)
        # signin= self.driver.find_element_by_link_text('Sign In')
        # signin.click()

        username = self.driver.find_element_by_name('fld-e')
        password = self.driver.find_element_by_name('fld-p1')

        username.send_keys(Lines[0])
        password.send_keys(Lines[1])

        submitBtnClick = WebDriverWait(self.driver,10)
        submitBtnClick = (submitBtnClick.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[4]")))).click()

        #WebDriverWait(self.driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        # submit_btn = self.driver.find_element_by_xpath("/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[4]")
        # submit_btn.click()
        time.sleep(5) # This is needed in order to let the whole page load so the cookies can be added
    
    def registerForQueue(self):
        boolean = True
        while boolean:
            try:
                print("trying this")
                addToCart_btn = self.driver.find_element_by_xpath("//button[normalize-space()='Add to Cart']");
                addToCart_btn.click()
                boolean = False
            except NoSuchElementException:
                k = random.randint(30, 45)
                print("sleeping now for " + str(k) + " seconds")
                time.sleep(k)
                self.driver.refresh()
                boolean = True

        print("registered for queue")

    def addToCart(self):
        boolean = True
        while boolean:
            try:
                print("waiting for last step")
                addToCart_btn = self.driver.find_element_by_xpath("//button[normalize-space()='Add to Cart']");
                addToCart_btn.click()
                print("final add to cart")
                time.sleep(3)
                checkout_btn = self.driver.find_element_by_xpath("//a[normalize-space()='Go to Cart']")
                checkout_btn.click()
                print("heading to checkout")
                boolean = False
            except NoSuchElementException:
                print("sleeping now for " + str(2) + " seconds")
                time.sleep(2)
                boolean = True
        print("ready to checkout")

if __name__ == "__main__":
    taskmaster = BestBuyAutomation()
    taskmaster.executeTest("bestbuyCookies.pkl", 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440')
