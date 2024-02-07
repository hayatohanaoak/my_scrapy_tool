import sqlite3
conn = sqlite3.connect('NIKKEI.db')
cur  = conn.cursor()
for i in cur.execute('''
select code, sup, inf 
from tbl_stock_prices
where code > 2000
and code < 2500
limit 10;
'''):
    print(i)