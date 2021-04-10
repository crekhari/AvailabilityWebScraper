from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
import random

class amdAutomation():

    def __init__(self):
        self.driver = None

    def setWebsiteLocation(self, link):
        self.driver = webdriver.Chrome('/Users/chiraag/chromedriver')
        self.driver.get(link)
        
    def executeTest(self, link):
        self.setWebsiteLocation(link)
        self.addToCart()

    def addToCart(self):
        i = 1
        while i == 1:
            try:
                print("trying this")
                addToCart_btn = self.driver.find_element_by_xpath("//button[contains(text(),'Add to Cart')]");
                addToCart_btn.click()
                i = 2
            except NoSuchElementException:
                print("sleeping now for " + str(3) + " seconds")
                time.sleep(3)
                self.driver.refresh()
                i = 1
        print("adding to cart :)")

if __name__ == "__main__":
    taskmaster = amdAutomation()
    taskmaster.executeTest('https://www.amd.com/en/direct-buy/5458372200/us')






#search = browser.find_element_by_name('st')
#search.send_keys("rtx 3080")

#search_btn = browser.find_element_by_xpath("/html/body/div[3]/main/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[1]/div/div/div[1]")
#search_btn.click()



'''

'''