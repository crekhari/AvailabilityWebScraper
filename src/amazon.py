from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import random,pickle,os,time,sys,requests


class AmazonAutomation():

    def __init__(self):
        self.driver = None

    def executeTest(self,file,link):
        response = requests.get(link)
        print(response.status_code)





if __name__ == "__main__":
    taskmaster = AmazonAutomation()
    taskmaster.executeTest("cookies.pkl", 'https://www.amazon.com/EVGA-GeForce-Technology-Backplate-24G-P5-3987-KR/dp/B08J5F3G18')