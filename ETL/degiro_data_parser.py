from database.config.column_mapping import column_name_mapping, column_type_mapping
from datetime import datetime

class DeGiroParser():
    def __init__(self):
        pass

    def parse(self, df_in, date: str):
        df = df_in.copy().rename(columns=column_name_mapping)

        df['product'] = self.parse_product(df['product'])
        df['symbol'] = self.parse_symbol(df['symbol'])
        df['count'] = self.parse_count(df['count'])
        df['closing_price'] = self.parse_closing_price(df['closing_price'])
        df['currency'] = self.parse_currency(df['value_local'])
        df['value_local'] = self.parse_value_local(df['value_local'])
        df['value_eur'] = self.parse_value_eur(df['value_eur'])
        df['create_dt'] = date

        return df.astype(column_type_mapping)
    
    def parse_product(self,df):
        return df
    
    def parse_symbol(self,df):
        return df
    
    def parse_count(self, df):
        return df.fillna(0).astype(int)
    
    def parse_closing_price(self,df):
        result =  df.replace(to_replace=r',', value='.', regex=True).astype(float)
        return result
    
    def parse_currency(self,df):
        return df.astype(str).str[:3]

    def parse_value_local(self,df):
        result = df.replace(to_replace=r'^EUR|USD|SEK', value='', regex=True).astype(float)
        return result
    
    def parse_value_eur(self,df):
        result =  df.replace(to_replace=r',', value='.', regex=True).astype(float)
        return result