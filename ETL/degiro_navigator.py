import os.path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from browser.selenium_driver import SeleniumDriver
import time


class DeGiroNavigator():

    BASE_URL = "https://trader.degiro.nl/trader4/#/markets"

    DOWNLOADS_PATH = os.getcwd() + '/data'

    def __init__(self):
        ## Setup chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless") # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1200")
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": self.DOWNLOADS_PATH  # Specify the directory to save downloads
        })

        # Set path to chromedriver as per your configuration
        homedir = os.path.expanduser("~")
        webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")

        driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
        self.driver = SeleniumDriver(driver)
        self.driver.driver.get(self.BASE_URL)


    def login(self):   
        # # Wait for cookies and accept
        cookie_id = "CybotCookiebotDialogBodyButtonDecline"
        element = self.driver.waitForElement(cookie_id)
        self.driver.elementClick(cookie_id)

        # # Login sequence
        self.driver.sendKeys(os.getenv('DEGIRO_USERNAME'), '//*[@id="username"]', 'xpath')
        self.driver.sendKeys(os.getenv('DEGIRO_PASSWORD'), '//*[@id="password"]', 'xpath')
        self.driver.elementClick('//*[@id="loginForm"]/div[4]/button', 'xpath')

        # Check if logged in
        self.driver.waitForElement("//*[@id=\"appContainer\"]/div/aside/nav[2]/div/button", 'xpath')

    def to_export_page(self):
        self.driver.elementClick('//*[@id=\"appContainer\"]/div/aside/nav[1]/a[3]', 'xpath')

        export_button_xpath = '//*[@id="mainContent"]/div[1]/section/div/section/div[1]/div/header/div/button'
        self.driver.waitForElement(export_button_xpath, 'xpath')
        self.driver.elementClick(export_button_xpath, 'xpath')

    def to_export_date(self, dateString: str):
        input_xpath = "/html/body/div[2]/div/div/div[2]/div/div[1]/input"
        self.driver.waitForElement(input_xpath, 'xpath', timeout=100)
        self.driver.elementClick(input_xpath, 'xpath')
        self.driver.clearElement(input_xpath, 'xpath')
        self.driver.sendKeys(dateString, input_xpath, 'xpath' )
        self.driver.sendKeys(Keys.ENTER, input_xpath, 'xpath')


    def download_csv(self, search_filename, rename_to_filename):
        csv_xpath = '/html/body/div[2]/div/div/div[2]/div/div[2]/a[3]'
        self.driver.waitForElement(csv_xpath, 'xpath', timeout=100)
        self.driver.elementClick(csv_xpath, 'xpath')

        time_waited = 0
        wait_time = 0.2
        while time_waited < 10:
            time.sleep(wait_time)
            if os.path.exists(self.DOWNLOADS_PATH + '/' + search_filename):
                os.rename(
                    self.DOWNLOADS_PATH + '/' + search_filename, 
                    self.DOWNLOADS_PATH + '/' + rename_to_filename
                    )
                break
            time_waited += wait_time
            

    def __enter__(self):
        return self
    
    def __exit__(self, ext_type=None, exc_value=None, traceback=None):
        self.driver.driver.quit()

