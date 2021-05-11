from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import random,pickle,os,time,sys


class AmazonAutomation():

    def __init__(self):
        self.driver = None




if __name__ == "__main__":
    taskmaster = AmazonAutomation()
    taskmaster.executeTest("cookies.pkl", 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440')