from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
import requests
import pytesseract
from PIL import Image

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
chrome.get("https://course.fcu.edu.tw/")

while True:
    if chrome.current_url == "https://course.fcu.edu.tw/Login.aspx" or chrome.current_url == "https://course.fcu.edu.tw/":

        email = chrome.find_element_by_id("ctl00_Login1_UserName")
        password = chrome.find_element_by_id("ctl00_Login1_Password")
        checkCode = chrome.find_element_by_id("ctl00_Login1_vcode")

        chrome.find_element_by_id("ctl00_Login1_UserName").clear()
        chrome.find_element_by_id("ctl00_Login1_Password").clear()
        chrome.find_element_by_id("ctl00_Login1_vcode").clear()

        validateCode = chrome.find_element_by_id('ctl00_Login1_Image1')
        validateCode.screenshot("images.jpg")
        # time.sleep(1.5)

        im = Image.open("images.jpg")
        new_img = im.resize((200, 88))
        imgGray = new_img.convert('L')

        # 設定閾值
        threshold = 142
        # 載入畫素點
        pixdata = imgGray.load()
        # 獲取圖片的寬高
        width, height = imgGray.size
        for y in range(height):
            for x in range(width):
                if pixdata[x, y] < threshold:
                    pixdata[x, y] = 0
                else:
                    pixdata[x, y] = 255
        # 檢視圖片
        binImg = imgGray
        vcode = pytesseract.image_to_string(binImg)

        email.send_keys('')
        password.send_keys('')
        checkCode.send_keys(vcode)
        time.sleep(1)
        chrome.find_element_by_xpath(
            '//*[@id="ctl00_Login1_LoginButton"]').click()
    else:
        break
