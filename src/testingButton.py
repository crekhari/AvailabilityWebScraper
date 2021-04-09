from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
import random


browser = webdriver.Chrome('/Users/chiraag/chromedriver')

browser.get('https://www.bestbuy.com/site/ring-wi-fi-video-doorbell-wired-black/6450309.p?skuId=6450309')


try:
    addToCart_btn = browser.find_element_by_xpath("//button[normalize-space()='Add to Cart']");
    addToCart_btn.click()
    print("clicked button")
    time.sleep(3)
    checkout_btn = browser.find_element_by_xpath("//a[normalize-space()='Go to Cart']")
    checkout_btn.click()
except NoSuchElementException:
    print("cant find button")



'''
//*[@id="fulfillment-add-to-cart-button-7631997"]/div/div/div/button
/html/body/div[3]/main/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[1]/div/div/div/button

//button[normalize-space()='Add to Cart']
//button[normalize-space()='Add to Cart']


<button class="btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button" type="button" 
data-sku-id="6450309" style="padding:0 8px"><svg aria-hidden="true" role="img" viewBox="0 0 100 100" 
style="width:16px;height:16px;margin-bottom:-2px;margin-right:9px;fill:currentColor"><use href="/~assets/bby/_img/int/plsvgdef-frontend/svg/cart.svg#cart" 
xlink:href="/~assets/bby/_img/int/plsvgdef-frontend/svg/cart.svg#cart"></use></svg>Add to Cart</button>
'''