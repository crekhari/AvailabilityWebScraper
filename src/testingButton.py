from os import link
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
import random

class testingButton():

    def __init__(self):
        self.driver = None

    def setWebsiteLocation(self, link):
        self.driver = webdriver.Chrome('/Users/chiraag/chromedriver')
        self.driver.get(link)
    
    def executeTest(self, link):
        self.setWebsiteLocation(link)
        parent = self.driver.current_window_handle
        self.openMultipleWindows()
        self.addToCartAndCheckout()

    def openMultipleWindows(self):
        allWindows = set()
        for x in range(3):
            self.driver.get('https://www.bestbuy.com/site/ring-wi-fi-video-doorbell-wired-black/6450309.p?skuId=6450309')
            
            allWindows.add(self.driver.current_window_handle)
            self.driver.switch_to_window(allWindows(x))


    def addToCartAndCheckout(self):
        try:
            addToCart_btn = self.driver.find_element_by_xpath("//button[normalize-space()='Add to Cart']");
            addToCart_btn.click()
            print("clicked button")
            time.sleep(3)
            checkout_btn = self.driver.find_element_by_xpath("//a[normalize-space()='Go to Cart']")
            checkout_btn.click()
        except NoSuchElementException:
            print("cant find button")

if __name__ == "__main__":
    taskmaster = testingButton()
    taskmaster.executeTest('https://www.bestbuy.com/site/ring-wi-fi-video-doorbell-wired-black/6450309.p?skuId=6450309')