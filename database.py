import pandas as pd
from model import engine

conn = engine.connect()

# drop_query="""DROP TABLE logs"""
# drop_query="""TRUNCATE TABLE  logs;"""
# conn.execute(drop_query)

df = pd.read_sql("""select * from catalog""", conn)
# df[['id', 'created_at', 'logger', 'message', 'level_name', 'module']].tail(10)

# df['logger'].value_counts()

# pd.set_option('display.max_columns', None)

df[['created_at', 'logger', 'message']].tail(20)