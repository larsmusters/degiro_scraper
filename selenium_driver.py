from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from logger import get_logger


class SeleniumDriver():
    def __init__(self, driver):
        self.driver = driver
        self.logger = get_logger(__name__)

    def getByType(self, locatorType):
            locatorType = locatorType.lower()
            if locatorType == "id":
                return By.ID
            elif locatorType == "name":
                return By.NAME
            elif locatorType == "xpath":
                return By.XPATH
            elif locatorType == "css":
                return By.CSS_SELECTOR
            elif locatorType == "class":
                return By.CLASS_NAME
            elif locatorType == "link":
                return By.LINK_TEXT
            else:
                self.logger.critical("Locator type " + locatorType + " not correct/supported")
            return False
    
    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            if not element.is_displayed:
                self.logger.critical("Element found is invisible, don't do anything with it: " + locator + " locatorType: " + locatorType)
                raise NoSuchElementException
            self.logger.info("Element Found with locator: " + locator + " and locatorType: " + locatorType)
        except:
            self.logger.critical("Element not found with locator: " + locator + " and  locatorType: " + locatorType)
        return element
    
    def elementClick(self, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            element.click()
            self.logger.info("Clicked on element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.logger.critical("Cannot click on the element with locator: " + locator + " locatorType: " + locatorType)
            print_stack()

    def sendKeys(self, data, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            element.send_keys(data)
            self.logger.info("Sent data on element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.logger.info("Cannot send data on the element with locator: " + locator + " locatorType: " + locatorType)
            print_stack()

    def waitForElement(self, locator, locatorType="id",
                               timeout=10, pollFrequency=0.5):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.logger.info("Waiting for maximum :: " + str(timeout) + " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout, poll_frequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.presence_of_element_located((byType, locator)))
            self.logger.info("Element appeared on the web page")
        except:
            self.logger.error("Element not appeared on the web page")
            print_stack()
        return element

    def waitForDownload(self, file_type: str ='.csv', timeout: int=10):
        try:
            self.logger.info("Waiting for maximum :: " + str(timeout) + " :: seconds for downloaded " + file_type + " to appear")
            WebDriverWait(self.driver, timeout).until(lambda driver: file_type in driver.title)
            self.logger.info("Download appeared")
        except NoSuchElementException:
            print('Download failed')