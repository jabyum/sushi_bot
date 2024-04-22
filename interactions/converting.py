import pandas as pd
import sqlite3
import random
from datetime import date
def convert_to_excel(table):
    conn = sqlite3.connect('data.db')
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    conn.close()
    name = f"{table}"+ str(date.today())+"_" + str(random.randint(1, 1000))
    df.to_excel(f'{name}.xlsx', index=False)
    return name
