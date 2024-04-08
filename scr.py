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
import csv



def scraping_individual(csvfile):
    laps_table = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="efforts-table"]/table')))
    name = driver.find_element(By.XPATH, '//*[@id="heading"]/header/h2/span/a').text
    rows_timeout = laps_table.find_elements(By.CSS_SELECTOR, 'tbody tr')
    headings = laps_table.find_elements(By.CSS_SELECTOR, 'thead th')
    laps_data = {heading.text: [] for heading in headings}
    # Loop through the rows
    for row in rows_timeout:
    # Find the cells in the row
        cells = row.find_elements(By.CSS_SELECTOR, 'td')
    # Loop through the cells and add the cell values to the corresponding key in the dictionary
        for b, cell in enumerate(cells):
            laps_data[list(laps_data.keys())[b]].append(cell.text)
    results.append({"Name": name, "Attributes": laps_data})
    with open('Draft.csv', mode='a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Attributes']  # Adjust the fieldnames accordingly
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({"Name": name, "Attributes": laps_data})




def scraping_data(csvfile):
    icon = driver.find_element(By.CLASS_NAME, "app-icon.icon-run.icon-lg")
    icon.click()
    print(icon)
    #FIND BEST EFFORTS TABLE
    ls = driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div[3]/div[2]/div[3]/div[1]/table/tbody[4]')
    # Find the elements for 5k, 10k, and 10 mile
    elements = ls.find_elements(By.XPATH,'//tr[td="5k" or td="10k" or td="10 mile"]')
    results = []
    athlete_name = driver.find_element(By.CLASS_NAME, 'athlete-name').text
    for element in elements:
        distance = element.find_element(By.XPATH, 'td[1]').text
        time = element.find_element(By.XPATH, 'td[2]').text
        results.append({'Athlete Name': athlete_name, 'Distance':[distance],'Time':[time]})


        


                            


