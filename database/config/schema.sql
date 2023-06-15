CREATE TABLE IF NOT EXISTS data(
    id integer primary key,
    product text,
    symbol text,
    count int,
    closing_price DECIMAL(10,2),
    currency text,
    value_local DECIMAL(10,2),
    value_eur DECIMAL(10,2),
    create_dt date
);