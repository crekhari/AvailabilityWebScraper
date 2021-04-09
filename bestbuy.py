from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
import random


browser = webdriver.Chrome('/Users/chiraag/chromedriver')

browser.get('https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440')

dropdown = browser.find_element_by_xpath("/html/body/div[2]/div/div/header/div[2]/div[2]/div/nav[2]/ul/li[1]/button/div[2]/span")
dropdown.click()
time.sleep(15)
signin= browser.find_element_by_link_text('Sign In')
signin.click()


username = browser.find_element_by_name('fld-e')
password = browser.find_element_by_name('fld-p1')

username.send_keys("crekhari@gmail.com")
password.send_keys("bestbuyDrlal12#")

submit_btn = browser.find_element_by_xpath("/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[4]")
submit_btn.click()

time.sleep(7)

i = 1
while i == 1:
    try:
        print("trying this")
        addToCart_btn = browser.find_element_by_xpath("//button[normalize-space()='Add to Cart']");
        addToCart_btn.click()
        i = 2
    except NoSuchElementException:
        k = random.randint(30, 45)
        print("sleeping now for " + str(k) + " seconds")

        time.sleep(k)
        browser.refresh()
        i = 1

print("adding to cart :)")

j = 1
while j == 1:
    try:
        print("waiting for last step")
        addToCart_btn = browser.find_element_by_xpath("//button[normalize-space()='Add to Cart']");
        addToCart_btn.click()
        print("final add to cart")
        time.sleep(3)
        checkout_btn = browser.find_element_by_xpath("//a[normalize-space()='Go to Cart']")
        checkout_btn.click()
        print("heading to checkout")
        j = 2
    except NoSuchElementException:
        print("sleeping now for " + str(2) + " seconds")
        time.sleep(2)
        j= 1

print("ready to checkout")





#search = browser.find_element_by_name('st')
#search.send_keys("rtx 3080")

#search_btn = browser.find_element_by_xpath("/html/body/div[3]/main/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[1]/div/div/div[1]")
#search_btn.click()



'''
<button class="btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button" type="button" data-sku-id="5199701" style="padding:0 8px"><svg aria-hidden="true" role="img" viewBox="0 0 100 100" style="width:16px;height:16px;margin-bottom:-2px;margin-right:9px;fill:currentColor"><use href="/~assets/bby/_img/int/plsvgdef-frontend/svg/cart.svg#cart" xlink:href="/~assets/bby/_img/int/plsvgdef-frontend/svg/cart.svg#cart"></use></svg>Add to Cart</button>
/html/body/div[2]/div/div/header/div[2]/div[2]/div/nav[2]/ul/li[1]/button/div[2]/span
//*[@id="account-tab"]
//*[@id="ABT2465Menu"]/header/a[1]
/html/body/div[2]/div/div/header/div[2]/div[2]/div/nav[2]/ul/li[1]/div/div/div[2]/header/a[1]
//*[@id="fulfillment-add-to-cart-button-17215176"]/div/div/div/button
/html/body/div[3]/main/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[1]/div/div/div/button
//*[@id="fulfillment-add-to-cart-button-40373596"]/div/div/div/button
/html/body/div[3]/main/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[1]/div/div/div/button
https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440
'''