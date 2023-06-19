## Run selenium and chrome driver to scrape data from cloudbytes.dev
import time
import pandas as pd
from dotenv import load_dotenv
from ETL.degiro_navigator import DeGiroNavigator
from ETL.degiro_data_parser import DeGiroParser
from database.database_handler import DatabaseHandler
from database.config.column_mapping import column_name_mapping
from datetime import datetime
import os
import random

load_dotenv()

DOWNLOADED_FILE_NAME = "Portfolio.csv"

class DataCollector():
    DATE_FORMAT = "%Y_%m_%d"
    DEGIRO_DATE_FORMAT = "%d/%m/%Y"

    def __init__(self, start_date):
        self.START_DATE = start_date
        self.navigator = DeGiroNavigator()
        self.navigator.login()
        self.navigator.to_export_page()

        self.database_handler = DatabaseHandler()


    def get_df_from_degiro(self, date: str, filename: str):
        self.navigator.to_export_date(date)
        self.navigator.download_csv(DOWNLOADED_FILE_NAME,filename + '.csv')

        try:
            df = pd.read_csv(f"{self.navigator.DOWNLOADS_PATH}/{filename}.csv")
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=[*column_name_mapping.keys()])
        return df


    def get_missing_dates(self) -> list[datetime]:
        all_dates = pd.date_range(self.START_DATE, datetime.now(), freq='d')
        filenames = os.listdir(os.getcwd() + '/data')
        present_dates = [datetime.strptime(filename.replace(".csv", ""), self.DATE_FORMAT) for filename in filenames]
        absent_dates = [date for date in all_dates if date not in present_dates]
        return absent_dates
    

    def get_missing_data(self) -> None:
        dates = self.get_missing_dates()
        parser = DeGiroParser()
        df_all = pd.DataFrame(columns=[*column_name_mapping.values()])
        for date in dates:
            df = self.get_df_from_degiro(date.strftime(self.DEGIRO_DATE_FORMAT), date.strftime(self.DATE_FORMAT))
            df = parser.parse(df, date.strftime(self.DATE_FORMAT))
            df_all = pd.concat([df_all, df], ignore_index=True)
            time.sleep(random.uniform(2,4))
        self.database_handler.insert_data(df_all)


    def __enter__(self):
        return self
    
    def __exit__(self, ext_type=None, exc_value=None, traceback=None):
        self.navigator.__exit__()
        self.database_handler.__exit__()

if __name__ == "__main__":
    collector = DataCollector(datetime(2023,1,1))
    dates = collector.get_missing_dates()
    print(dates)