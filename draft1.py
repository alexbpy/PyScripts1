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


class Login:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def login(self):

        vpn_ip = "185.107.56.215"


        chrome_options = webdriver.ChromeOptions()
        proxy_address = f'http://{vpn_ip}:80'  # Replace '8080' with the actual port number
        chrome_options.add_argument(f'--proxy-server={proxy_address}')
        driver = webdriver.Chrome(options=chrome_options)


        driver = webdriver.Chrome()
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


class Scraping:
    def __init__(self, driver):
        self.driver=driver
        
    def scraping(self):
        driver = self.driver
        
        #For scraping past first few pages
        for page in range(1,258):
            current_window = driver.current_window_handle
            next_page = driver.find_element(By.XPATH, '//*[@id="results"]/nav/ul')
            next = next_page.find_element(By.CSS_SELECTOR, 'li.next_page > a[rel="next"]').click()
            time.sleep(2.5)
            # k += 1
        
        results= []
        data = {}
        k = 3
        
        with open('Draft.csv', mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Attributes']  # Adjust the fieldnames accordingly
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()  # Write the CSV header
        
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
            # writer.writerow({"Name": name, "Attributes": laps_data})
        # Initialize a CSV file and writer to save the data at each iteration


        
        while True:
            try:
                table = driver.find_element(By.XPATH, '//*[@id="results"]/table/tbody')
                rows = table.find_elements(By.CSS_SELECTOR, 'tr')
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
                        current_window = driver.current_window_handle
                        wait = WebDriverWait(driver, 5)
                        #first, click on the relevant segment link
                        url = table.find_element(By.XPATH, f'//*[@id="results"]/table/tbody/tr[{i+1}]/td[3]/a')
                        url.send_keys(Keys.CONTROL + Keys.RETURN)
                        handles = driver.window_handles
                        driver.switch_to.window(handles[-1])
                        driver.find_element(By.LINK_TEXT, 'Laps').click()
                        # Switch to the new window again
                        handles = driver.window_handles
                        driver.switch_to.window(handles[-1])
                        scraping_individual(csvfile)
                        i += 1
                        print(i)
                        print(results[-1])
                        #print(f'{i} done')
                    except TimeoutException:
                        driver.find_element(By.XPATH, '//*[@id="pagenav"]/li[1]/a').click()
                        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="map-canvas"]')))
                        time.sleep(1)
                        # Switch to the new window again
                        driver.switch_to.window(driver.current_window_handle)
                        driver.find_element(By.LINK_TEXT, 'Laps').click()
                        # Switch to the new window again
                        driver.switch_to.window(driver.current_window_handle)
                        scraping_individual(csvfile)
                        i += 1
                        print(i)
                        print(results[-1])
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
                            i += 1
                            print(i)

                        except NoSuchElementException:
                            print('No Lap Data Available')
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
                    time.sleep(100)
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
    
        df = pd.DataFrame(results)
        print(f'dataframe is :{df}')
#         df.to_csv('Strava_Overall_Test_Page232-250', header=True, index = False)
        
# login_obj = Login('j7967362@gmail.com', 'fruit12fan')
login_obj = Login("alexpythonb3@gmail.com", "oi12ytre")
driver = login_obj.login()

load_obj = LoadPage(driver)
load_obj.load()

load_scrape = Scraping(driver)
load_scrape.scraping()
