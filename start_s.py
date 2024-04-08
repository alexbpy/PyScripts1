from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchWindowException
import pandas as pd



driver = webdriver.Chrome(executable_path=r"C:\Users\alexb\Downloads\chromedriver-win32\chromedriver-win32\chromedriver.exe")
driver.get("https://www.google.com")
driver.maximize_window()
time.sleep(5)
lucky = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[4]/center/input[2]')
lucky.send_keys(Keys.CONTROL + Keys.RETURN)
