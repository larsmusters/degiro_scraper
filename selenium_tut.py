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

load_dotenv()

t = time.time()
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

# Choose Chrome Browser
browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# Get page
browser.get("https://trader.degiro.nl/trader4/#/markets")

# If there are cookies, accept them
try: 
    cookie_id = 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll'
    element = WebDriverWait(browser, 10).until(expected_conditions.presence_of_element_located((By.ID, cookie_id)))
    accept_cookies = browser.find_element(By.ID, cookie_id).click()
except NoSuchElementException:
    print("couldn't find cookie element")

# Login sequence
try:
    time.sleep(random.uniform(1,2))
    login = browser.find_element(By.XPATH, '//*[@id="username"]')
    if login.is_displayed():
        login.send_keys(os.getenv('DEGIRO_USERNAME'))
    else:
        raise NoSuchElementException('Found an invisible username field?')

    time.sleep(random.uniform(1,2))
    password = browser.find_element(By.XPATH, '//*[@id="password"]')
    if password.is_displayed():
        password.send_keys(os.getenv('DEGIRO_PASSWORD'))
    else:
        raise NoSuchElementException('Found an invisible password field?')

    time.sleep(random.uniform(1,2))
    submit = browser.find_element(By.XPATH, '//*[@id="loginForm"]/div[4]/button')
    if submit.is_displayed():
        submit.click()
    else:
        raise NoSuchElementException('Found an invisible submit button?')
except NoSuchElementException as e:
    print("Some element was not found:", str(e))

# Test if logged in
try:
    time.sleep(2)
    logout_button = browser.find_element(By.XPATH, "//*[@id=\"appContainer\"]/div/aside/nav[2]/div/button")
    if not logout_button.is_displayed:
        raise NoSuchElementException('Invisible Logout button')
    print('Successfully logged in')
except NoSuchElementException:
    print('Incorrect login/password')

# Navigate to export page
try:
    time.sleep(random.uniform(1,2))
    portefeille_button_xpath = '//*[@id=\"appContainer\"]/div/aside/nav[1]/a[3]'
    portefeuille_button = WebDriverWait(browser, 10).until(expected_conditions.presence_of_element_located((By.XPATH, portefeille_button_xpath)))
    # portefeille_button = browser.find_element(By.XPATH, portefeille_button_xpath)
    if not portefeuille_button.is_displayed:
        raise NoSuchElementException('Invisible portefeuille button')
    portefeuille_button.click()

    time.sleep(random.uniform(1,2))
    export_button_xpath = '//*[@id="mainContent"]/div[1]/section/div/section/div[1]/div/header/div/button'
    export_button = WebDriverWait(browser, 10).until(expected_conditions.presence_of_element_located((By.XPATH, export_button_xpath)))
    # export_button = browser.find_element(By.XPATH, export_button_xpath)
    if not export_button.is_displayed:
        raise NoSuchElementException('Invisible export button')
    export_button.click()

    time.sleep(random.uniform(1,2))
    csv_xpath = '/html/body/div[3]/div/div/div[2]/div/div[2]/a[3]'
    csv_button = WebDriverWait(browser, 10).until(expected_conditions.presence_of_element_located((By.XPATH, csv_xpath)))
    # csv_button = browser.find_element(By.XPATH, csv_xpath)
    if not csv_button.is_displayed:
        raise NoSuchElementException('Invisible csv button')
    csv_button.click()

    WebDriverWait(browser, 10).until(lambda driver: ".csv" in browser.title)
except NoSuchElementException:
    print('Could not navigate to export page')

time.sleep(10)
browser.quit()