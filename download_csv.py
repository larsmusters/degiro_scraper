## Run selenium and chrome driver to scrape data from cloudbytes.dev
import time
from dotenv import load_dotenv
from degiro_navigator import DeGiroNavigator

load_dotenv()

navigator = DeGiroNavigator()
navigator.login()
navigator.to_export_page()
navigator.download_csv()

time.sleep(10)
navigator.exit()