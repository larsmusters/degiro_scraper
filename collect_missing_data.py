## Run selenium and chrome driver to scrape data from cloudbytes.dev
import time
import pandas as pd
from dotenv import load_dotenv
from ETL.degiro_navigator import DeGiroNavigator
from ETL.degiro_data_parser import DeGiroParser
from database.database_handler import DatabaseHandler
from database.config.column_mapping import column_name_mapping
from datetime import datetime

load_dotenv()

DOWNLOADED_FILE_NAME = "Portfolio.csv"

class DataCollector():
    START_DATE = datetime(2023, 4, 1)

    def __init__(self):
        dates = self.get_missing_dates()

        self.navigator = DeGiroNavigator()
        self.navigator.login()
        self.navigator.to_export_page()

        self.database_handler = DatabaseHandler()


    def get_df_from_degiro(self, date: str):
        date_string = date.replace("/", "_")
        filename = f"{date_string}.csv"
        self.navigator.to_export_date(date)
        self.navigator.download_csv(DOWNLOADED_FILE_NAME,filename)

        try:
            df = pd.read_csv(f"{self.navigator.DOWNLOADS_PATH}/{filename}")
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=[*column_name_mapping.keys()])
        return df

    def get_missing_dates(self) -> list[str]:
        date_range = pd.date_range(self.START_DATE, datetime.now(), freq='d')
        dates = [date.strftime("%m/%d/%Y") for date in date_range]
        return dates
    

    def get_missing_data(self) -> None:
        dates = self.get_missing_dates()
        parser = DeGiroParser()
        df_all = pd.DataFrame(columns=[*column_name_mapping.values()])
        for date in dates:
            df = self.get_df_from_degiro(date)
            df = parser.parse(df)
            df_all = pd.concat([df_all, df], ignore_index=True)
            time.sleep(3)
        self.database_handler.insert_data(df_all)


    def __enter__(self):
        return self
    
    def __exit__(self, ext_type=None, exc_value=None, traceback=None):
        self.navigator.__exit__()
        self.database_handler.__exit__()

if __name__ == "__main__":
    collector = DataCollector()
    dates = collector.get_missing_dates()
    print(dates)