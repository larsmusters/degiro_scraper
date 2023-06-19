from database.database_handler import DatabaseHandler
import numpy as np 

database_handler = DatabaseHandler()
# df = database_handler.get_data_by_name('VANGUARD FTSE AW')
df = database_handler.get_all_data()
# database_handler.empty_db()
# print(df)
print('Memory usage:',np.round(df.memory_usage(index=True).sum()/1000), 'KB')