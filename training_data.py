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
import traceback


class Login:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def login(self):

        # vpn_ip = "185.107.56.215"
        # chrome_options = webdriver.ChromeOptions()
        # proxy_address = f'http://{vpn_ip}:80'  # Replace '8080' with the actual port number
        # chrome_options.add_argument(f'--proxy-server={proxy_address}')
        # driver = webdriver.Chrome(options=chrome_options)

        driver = webdriver.Chrome(executable_path=r"C:\Users\alexb\Downloads\chromedriver-win32\chromedriver-win32\chromedriver.exe")
        driver.get("https://www.strava.com/login")
        driver.maximize_window()
        email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
        email_field.send_keys(self.email)
        
        password_field = driver.find_element(By.NAME,"password")
        password_field.send_keys(self.password)
        
        login_button = driver.find_element(By.XPATH, '//*[@id="login-button"]')
        login_button.click()
        
        return driver
    
class LoadPage:
    def __init__(self, driver):
        self.driver = driver
        
    def load(self):
        driver = self.driver
        driver.get("https://www.strava.com/segments/22100462")
        #TEST SEGMENT
        #driver.get('https://www.strava.com/segments/26847273') 

class Pagination:
    def __init__(self, driver):
        self.driver = driver

    def next_page(self):
        driver = self.driver
        for page in range(1,149):
            current_window = driver.current_window_handle
            next_page = driver.find_element(By.XPATH, '//*[@id="results"]/nav/ul')
            next = next_page.find_element(By.CSS_SELECTOR, 'li.next_page > a[rel="next"]').click()
            time.sleep(4)

class Scraping:
    def __init__(self, driver):
        self.driver=driver


        
    def scraping(self):
        driver = self.driver



        results= []
        k = 3
        
        def scraping_data():
            icon = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "app-icon.icon-run.icon-lg")))
            # icon = driver.find_element(By.CLASS_NAME, "app-icon.icon-run.icon-lg")
            icon.click()
            print(icon)
            #FIND BEST EFFORTS TABLE
            tablee = driver.find_element(By.CLASS_NAME,'dense.striped')
            mini_t = tablee.find_elements(By.TAG_NAME, 'tbody')
            ls = mini_t[3]
            # print(ls.text)
            # ls = driver.find_element(By.XPATH, "//span[@data-glossary-term='definition-best-efforts']/ancestor::table")
            # Find the elements for 5k, 10k, and 10 mile
            elements = ls.find_elements(By.XPATH,'//tr[td="5k" or td="10k" or td="10 mile"]')

            year_run = driver.find_element(By.ID, 'sport-0-ytd')
            print(year_run.text)

            column_activity = [elem.text for elem in year_run.find_elements(By.XPATH, '//tr[td="Activities"]/td[2]') if elem.text.strip()]
            column_distance = [elem.text for elem in year_run.find_elements(By.XPATH, '//tr[td="Distance"]/td[2]') if elem.text.strip()]
            column_time = [elem.text for elem in year_run.find_elements(By.XPATH, '//tr[td="Time"]/td[2]') if elem.text.strip()]

            # column_activity = year_run.find_elements(By.XPATH, '//tr[td="Activities"]/td[2]')
            # column_distance = year_run.find_elements(By.XPATH, '//tr[td="Distance"]/td[2]')
            # column_time = year_run.find_elements(By.XPATH, '//tr[td="Time"]/td[2]')

            athlete_name = driver.find_element(By.CLASS_NAME, 'text-title1.athlete-name').text

            for activity, distance, time in zip(column_activity, column_distance, column_time):
                data1 = activity
                data2 = distance
                data3 = time
                
                results.append({'Athlete Name':athlete_name, 'Activity':data1, 'Distance':data2, 'Time':data3})
                with open('Draft3.csv', mode='a', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Athlete Name','Activity', 'Distance', 'Time']  # Adjust the fieldnames accordingly
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerow({"Athlete Name": athlete_name,'Activity':data1, 'Distance':data2, 'Time':data3})               
                    
            for element in elements:
                distance = element.find_element(By.XPATH, 'td[1]').text
                print(distance)
                time = element.find_element(By.XPATH, 'td[2]').text
                print(time)
                results.append({'Athlete Name': athlete_name, 'Distance':distance,'Time':time})
                with open('Draft4.csv', mode='a', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Athlete Name', 'Distance', 'Time']  # Adjust the fieldnames accordingly
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerow({"Athlete Name": athlete_name, "Distance": distance, 'Time':time})

        while True:
            try:
                table = driver.find_element(By.XPATH, '//*[@id="results"]/table/tbody')
                rows = table.find_elements(By.CSS_SELECTOR, 'tr')
                print('foundtherows')
                time.sleep(3)
                #print(len(rows))
                i = 0
                outer_break = False
            except NoSuchWindowException:
                outer_break = True
                print('Breaking...')

            while i < len(rows):
                for row in rows:
                    try:
                        #print(i)
                        print('trying...')
                        current_window = driver.current_window_handle
                        wait = WebDriverWait(driver, 8)
                        time.sleep(4)
                        current_window
                        #first, click on the relevant segment link
                        parent = table.find_element(By.XPATH, f'/html/body/div[2]/div[3]/div[1]/div[2]/div[1]/table/tbody/tr[{i+1}]/td[2]')
                        n = parent.find_element(By.TAG_NAME, 'a')
                        href_link = n.get_attribute('href')
                        print('url found')
                        print(href_link)
                        driver.execute_script("window.open('', '_blank');")
                        time.sleep(2.5)
                        driver.switch_to.window(driver.window_handles[-1])
                        driver.get(href_link)
                        #####
                        current_url = driver.current_url
                        print(current_url)
                        scraping_data()
                        print(results)

                        time.sleep(5)
                        handles = driver.window_handles
                        driver.switch_to.window(handles[-1])
                        # scraping_individual()
                        i += 1
                        print(i)
                        print(f'switched to {i}')
                        #print(f'{i} done')
                    except TimeoutException:
                        # driver.find_element(By.XPATH, '//*[@id="pagenav"]/li[1]/a').click()
                        # wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="map-canvas"]')))
                        # time.sleep(1)
                        # # Switch to the new window again
                        # driver.switch_to.window(driver.current_window_handle)
                        # driver.find_element(By.LINK_TEXT, 'Laps').click()
                        # # Switch to the new window again
                        # driver.switch_to.window(driver.current_window_handle)
                        # scraping_individual()
                        i += 1
                        print(i)
                        print('timeout')
                    except TimeoutException:
                        i += 1
                        print('Timeout after Timeout')
                        #print(f'{i} timeout done')
                    except NoSuchWindowException:
                        outer_break = True
                        print('Breaking...')
                        break

                    except NoSuchElementException:
                        try:
                            # driver.find_element(By.LINK_TEXT, 'Race Analysis')
                            # name = driver.find_element(By.XPATH, '//*[@id="heading"]/header/h2/span/a').text
                            # race_analysis = driver.find_element(By.XPATH, '//*[@id="run-efforts-table"]/section/table')
                            # rows_exception = race_analysis.find_elements(By.CSS_SELECTOR, 'tbody tr')
                            # headings = race_analysis.find_elements(By.CSS_SELECTOR, 'thead th')
                            # laps_data = {heading.text: [] for heading in headings}
                            # for row in rows_exception:
                            #     cells = row.find_elements(By.CSS_SELECTOR, 'td')
                            # # Loop through the cells and add the cell values to the corresponding key in the dictionary
                            #     for b, cell in enumerate(cells):
                            #         laps_data[list(laps_data.keys())[b]].append(cell.text)
                            # results.append({"Name": name, "Attributes": laps_data})
                            current_url = driver.current_url
                            print(f'{current_url} for no such element')
                            i += 1
                            print(i)
                            print('nosuchelement')
                            traceback.print_exc()
                            # print(results[-1])
                            #print(f'{i} nosuchelement done')
                        except NoSuchElementException:
                            #print('No Lap Data Available')
                            i += 1
                        except TimeoutException:
                            i += 1
                    finally: 
                        try:
                            driver.close()
                            time.sleep(3)
                            #driver.execute_script("window.history.go(-1)")
                            driver.switch_to.window(handles[0])
                        except WebDriverException:
                            outer_break = True
                            break
                    if outer_break:
                        break

                try:
                    #To go to next page
                    next_page = driver.find_element(By.XPATH, '//*[@id="results"]/nav/ul')
                    next = next_page.find_element(By.CSS_SELECTOR, 'li.next_page > a[rel="next"]').click()
                    time.sleep(40)
                    k += 1
                except NoSuchElementException:
                    #print('No Next Page')
                    outer_break = True
                    break
                except NoSuchWindowException:
                    outer_break = True
                    break

            if outer_break:
                break
                print(f'break at number {i} on page {k-2}')
        # if outer_break:
        #     break
    
    
        # df = pd.DataFrame(results)
        # print(f'dataframe is :{df}')
        # df.to_csv('Name_Test', header=True, index = False)
        
# login_obj = Login("alexpythonb3@gmail.com", "oi12ytre")
login_obj = Login("alex.brader123@gmail.com", "oi12ytre")
driver = login_obj.login()

load_obj = LoadPage(driver)
load_obj.load()

load_page = Pagination(driver)
load_page.next_page()

load_scrape = Scraping(driver)
load_scrape.scraping()

