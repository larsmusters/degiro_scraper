## Run selenium and chrome driver to scrape data from cloudbytes.dev
import time
from dotenv import load_dotenv
from collect_missing_data import DataCollector

load_dotenv()

with DataCollector() as collector:
    collector.get_missing_data()
