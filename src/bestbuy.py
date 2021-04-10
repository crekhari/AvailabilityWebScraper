from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
import random

class bestbuyAutomation():

    def __init__(self):
        self.driver = None

    def setWebsiteLocation(self, link):
        self.driver = webdriver.Chrome('/Users/chiraag/chromedriver')
        self.driver.get(link)

    def executeTest(self, link):
        self.setWebsiteLocation(link)
        self.login()
        self.registerForQueue()
        self.addToCart()

    def login(self):
        dropdown = self.driver.find_element_by_xpath("/html/body/div[2]/div/div/header/div[2]/div[2]/div/nav[2]/ul/li[1]/button/div[2]/span")
        dropdown.click()
        time.sleep(15)
        signin= self.driver.find_element_by_link_text('Sign In')
        signin.click()

        username = self.driver.find_element_by_name('fld-e')
        password = self.driver.find_element_by_name('fld-p1')

        username.send_keys("crekhari@gmail.com")
        password.send_keys("bestbuyDrlal12#")

        submit_btn = self.driver.find_element_by_xpath("/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[4]")
        submit_btn.click()

        time.sleep(7)
    
    def registerForQueue(self):
        i = 1
        while i == 1:
            try:
                print("trying this")
                addToCart_btn = self.driver.find_element_by_xpath("//button[normalize-space()='Add to Cart']");
                addToCart_btn.click()
                i = 2
            except NoSuchElementException:
                k = random.randint(30, 45)
                print("sleeping now for " + str(k) + " seconds")

                time.sleep(k)
                self.driver.refresh()
                i = 1

        print("registered for queue")

    def addToCart(self):
        j = 1
        while j == 1:
            try:
                print("waiting for last step")
                addToCart_btn = self.driver.find_element_by_xpath("//button[normalize-space()='Add to Cart']");
                addToCart_btn.click()
                print("final add to cart")
                time.sleep(3)
                checkout_btn = self.driver.find_element_by_xpath("//a[normalize-space()='Go to Cart']")
                checkout_btn.click()
                print("heading to checkout")
                j = 2
            except NoSuchElementException:
                print("sleeping now for " + str(2) + " seconds")
                time.sleep(2)
                j= 1

        print("ready to checkout")

if __name__ == "__main__":
    taskmaster = bestbuyAutomation()
    taskmaster.executeTest('https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440')