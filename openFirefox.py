import pickle
from selenium import webdriver
import pyautogui
from pathlib import Path
import pandas as pd


#------------------------------------------------------------------------------------------------------------------------------------------------
#webdriver firefox with profile

path_config = Path(__file__).with_name('configSelenium.json')
paths = pd.read_json(path_config)

myprofile = webdriver.FirefoxProfile(paths["Paths"]["Profile"])

driver = webdriver.Firefox(firefox_profile=myprofile,executable_path=paths["Paths"]["Geckodriver"])
#firefox_profile=myprofile,


#------------------------------------------------------------------------------------------------------------------------------------------------
#zabbix loading and adding cookies

driver.get("https://zabbix.bobbie.de/zabbix.php?action=dashboard.view")

cookies = pickle.load(open(Path(__file__).with_name('cookiesZabbix.pkl'), "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)

driver.refresh()


#------------------------------------------------------------------------------------------------------------------------------------------------
#hubspot loading and adding cookies

driver.get("https://app.hubspot.com/reports-dashboard/9232473/view/8219673")

cookies = pickle.load(open(Path(__file__).with_name('cookiesHubspot.pkl'), "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)

driver.refresh()


#------------------------------------------------------------------------------------------------------------------------------------------------
#connect to dashboard

driver.get("http://127.0.0.1:8050/")


#------------------------------------------------------------------------------------------------------------------------------------------------
#make fullscreen

pyautogui.press('f11')


#------------------------------------------------------------------------------------------------------------------------------------------------
