import pandas as pd
from sqlalchemy import create_engine

# fetch data from ny taxi website 
url = 'https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.parquet'
df = pd.read_parquet(url, engine = "fastparquet")

# connecting to postgres
user = 'root'
pwd = 'root'
db_name = 'ny_taxi'
port = 5432
host = 'localhost'

engine = create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{db_name}')
conn = engine.connect()

# create table with column names in postgres
df.head(n = 0).to_sql(name = 'yellow_taxi_data', con = conn, if_exists = 'replace', index = False)

# push the rest of data into table 
df.to_sql(name = 'yellows_taxi_data', con = conn, if_exists = 'append', index = False)

# close connex
conn.close()