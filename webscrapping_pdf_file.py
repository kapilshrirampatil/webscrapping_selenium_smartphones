from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException

download_folder = "pdf_new"
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": os.path.abspath(download_folder),  # Change to your path
    "plugins.always_open_pdf_externally": True  # Ensures PDF is downloaded externally, not opened in browser
}
options.add_experimental_option("prefs", prefs)

# Path to your chromedriver executable
driver_path = r"C:/Users/admin/Downloads/chromedriver-win64/chromedriver.exe"  # Update with the path to your chromedriver
service = Service(driver_path)

# Initialize the ChromeDriver with options
driver = webdriver.Chrome(service=service, options=options)

# Open BSE Corporate Announcements page
driver.get("https://www.bseindia.com/corporates/ann.html")
time.sleep(3)

count = 0
while True:

    driver.find_element(By.CLASS_NAME, 'td' )

    html = driver.page_source

    with open("table.html",'w') as f:
        f.write(html)


    with open('table.html','r',encoding='utf-8',errors="ignore") as f:
        html = f.read()

    soup = BeautifulSoup(html,'html5lib')

    list_1 = []
    for i in soup.find_all('a',class_ = 'tablebluelink'):
        link = i.get('href')
        list_1.append(link.strip().strip("#"))

    print(list_1,len(list_1))

    for i in list_1[1:]:
        try:
            if i.endswith('.pdf'):
                base_link = 'https://www.bseindia.com'
                link = i
                fin_link = base_link + link
                driver.get(fin_link)
                time.sleep(10)  # Wait for the download to complete

                # Check if the file is downloaded
                print("PDF should be downloaded now!")
            time.sleep(2)
        except Exception as e:
            print(f'link is not avilable')
    try:
        # Scroll into view and ensure button is clickable
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'idnext'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        time.sleep(2)  # Allow slight delay for UI stabilization

        # Attempt to click the button
        ActionChains(driver).move_to_element(next_button).click().perform()
        time.sleep(3)  # Wait for the next page to load
        count = count+1
        print(count)
        
    except TimeoutException:
        print("Timeout: Next button not found or clickable. Reached the last page.")
        break
    except ElementClickInterceptedException:
        print("ElementClickInterceptedException: Retrying with JavaScript click.")
        driver.execute_script("arguments[0].click();", next_button)
    except NoSuchElementException:
        print("No 'Next' button found. Reached the last page.")
        break

# Perform any additional data scraping or processing here after reaching the last page
print("Finished iterating through all pages.")

