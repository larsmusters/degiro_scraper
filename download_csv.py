## Run selenium and chrome driver to scrape data from cloudbytes.dev
import time
import pandas as pd
from dotenv import load_dotenv
from ETL.degiro_navigator import DeGiroNavigator
from ETL.degiro_data_parser import DeGiroParser
from database.database_handler import DatabaseHandler
load_dotenv()

# with DeGiroNavigator() as navigator:
#     navigator.login()
#     navigator.to_export_page()
#     navigator.download_csv('Portfolio.csv','new_file.csv')

## Store data in table
# Read data from csv
filename='data/new_file.csv'
df = pd.read_csv(filename)

parser = DeGiroParser()
df = parser.parse(df)

database_handler = DatabaseHandler()
database_handler.empty_db()
database_handler.insert_data(df)
df = database_handler.get_data_by_name('VANGUARD FTSE AW')
# df = database_handler.get_all_data()
