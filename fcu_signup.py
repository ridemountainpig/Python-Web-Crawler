from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
import requests
import pytesseract
import cv2
from PIL import Image

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
chrome.get("https://signin.fcu.edu.tw/clockin/login.aspx")

email = chrome.find_element_by_id("LoginLdap_UserName")
password = chrome.find_element_by_id("LoginLdap_Password")

email.send_keys("")
password.send_keys("")

chrome.find_element_by_xpath('//*[@id="LoginLdap_LoginButton"]').click()
chrome.find_element_by_xpath('//*[@id="ButtonClassClockin"]').click()

while True:
    if chrome.current_url == "https://signin.fcu.edu.tw/clockin/ClassClockin.aspx":
        validateCode = chrome.find_element_by_xpath('//*[@id="form1"]/div[3]/img[2]')
        validateCode.screenshot("images.jpg")
        time.sleep(0.5)

        im = Image.open("images.jpg")
        new_img = im.resize((100, 44))
        imgGray = new_img.convert('L')
        
        #設定閾值
        threshold = 160
        #載入畫素點
        pixdata = imgGray.load()
        #獲取圖片的寬高
        width, height = imgGray.size
        for y in range(height):
            for x in range(width):
                if pixdata[x, y] < threshold:
                    pixdata[x, y] = 0
                else:
                    pixdata[x, y] = 255
        #檢視圖片
        binImg  = imgGray
        vcode = pytesseract.image_to_string(binImg)
        
        vaildateCode = chrome.find_element_by_id("validateCode")
        vaildateCode.clear()
        vaildateCode.send_keys(vcode)
        
        time.sleep(1)
        # chrome.refresh()
        chrome.find_element_by_xpath('//*[@id="Button0"]').click()
    else:
        break