
column_name_mapping = {
    'Product': 'product', 
    'Symbool/ISIN': 'symbol', 
    'Aantal': 'count', 
    'Slotkoers':'closing_price', 
    'Lokale waarde': 'value_local', 
    'Waarde in EUR': 'value_eur'
}

column_type_mapping = {
    'product': 'object',
    'symbol': 'object', 
    'count': 'int32',
    'closing_price': 'float64',
    'value_local': 'float64',
    'value_eur': 'float64',
    'create_dt': 'object'
}