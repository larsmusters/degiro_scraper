## Run selenium and chrome driver to scrape data from cloudbytes.dev
import time
from dotenv import load_dotenv
import random
import os.path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium_driver import SeleniumDriver
from logger import get_logger

load_dotenv()

## Setup chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless") # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1200")
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": os.getcwd() + '/csv'  # Specify the directory to save downloads
})

# Set path to chromedriver as per your configuration
homedir = os.path.expanduser("~")
webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")


BASE_URL = "https://trader.degiro.nl/trader4/#/markets"

browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)
driver = SeleniumDriver(browser)
driver.driver.get(BASE_URL)

# # Wait for cookies and accept
cookie_id = "CybotCookiebotDialogBodyButtonDecline"
element = driver.waitForElement(cookie_id)
driver.elementClick(cookie_id)

# # Login sequence
driver.sendKeys(os.getenv('DEGIRO_USERNAME'), '//*[@id="username"]', 'xpath')
driver.sendKeys(os.getenv('DEGIRO_PASSWORD'), '//*[@id="password"]', 'xpath')
driver.elementClick('//*[@id="loginForm"]/div[4]/button', 'xpath')

# Check if logged in
driver.waitForElement("//*[@id=\"appContainer\"]/div/aside/nav[2]/div/button", 'xpath')

# # Navigate to export page
driver.elementClick('//*[@id=\"appContainer\"]/div/aside/nav[1]/a[3]', 'xpath')

export_button_xpath = '//*[@id="mainContent"]/div[1]/section/div/section/div[1]/div/header/div/button'
driver.waitForElement(export_button_xpath, 'xpath')
driver.elementClick(export_button_xpath, 'xpath')

csv_xpath = '/html/body/div[3]/div/div/div[2]/div/div[2]/a[3]'
driver.waitForElement(csv_xpath, 'xpath')
driver.elementClick(csv_xpath, 'xpath')

#     WebDriverWait(browser, 10).until(lambda driver: ".csv" in browser.title)
# except NoSuchElementException:
#     print('Could not navigate to export page')

time.sleep(10)
browser.quit()