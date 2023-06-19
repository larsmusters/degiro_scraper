## Run selenium and chrome driver to scrape data from cloudbytes.dev
import time
from dotenv import load_dotenv
from collect_missing_data import DataCollector
from datetime import datetime

load_dotenv()

START_DATE = datetime(2023, 1, 1)


with DataCollector(START_DATE) as collector:
    collector.get_missing_data()
