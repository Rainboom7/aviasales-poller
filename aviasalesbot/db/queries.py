SQL_CREATE_TABLES = """
    create table if not exists avia_prices (
        id serial not null,
        fly_key varchar(100) not null ,
        price integer,
        fly_date varchar(100),
        link varchar(500)
    );
"""

SQL_CALCULATE_MIN_PRICE = """
SELECT min(price) from avia_prices where fly_key = %(fly_key)s
"""

SQL_CALCULATE_TOTAL_MIN_PRICE = """
SELECT SUM(min_price) AS total_sum
FROM (
    SELECT MIN(price) AS min_price
    FROM avia_prices
    WHERE fly_key = ANY(%(parameter_array)s)
    GROUP BY fly_key
) AS subquery;
"""

SQL_INSERT_NEW_PRICE = """
insert into avia_prices(fly_key,price,fly_date,link)
 values(%(fly_key)s,%(price)s,%(fly_date)s,%(link)s) 
"""
