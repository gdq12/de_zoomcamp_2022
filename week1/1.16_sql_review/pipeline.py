import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# fetch data from ny taxi website
print(f"fetching jan 2021 nyc taxi data on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
url = 'https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.parquet'
df = pd.read_parquet(url, engine = "fastparquet")

# fetch lookup table
print(f"fetching taxi look up data on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
url1 = 'https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv'
df1 = pd.read_csv(url1)

# connecting to postgres
user = 'postgres'
pwd = 'root'
db_name = 'postgres'
port = 5432
host = 'localhost'

print(f"connecting to postgres docker container on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
engine = create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{db_name}')
conn = engine.connect()

print(f"creating a new database on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}" )
db_name = 'ny_taxi'
conn.execute('commit')
conn.execute(f'create database {db_name}')
conn.execute('commit')
conn.close()

print(f"connecting to postgres docker container on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
engine = create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{db_name}')
conn = engine.connect()

# create table with column names in postgres
print(f"creating yellow_taxi_data table in postgres container on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
df.head(n = 0).to_sql(name = 'yellow_taxi_data', con = conn, if_exists = 'replace', index = False)

# create zone tablein postgres
print(f"creating taxi zone lookup table in postgres container on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
df1.head(n = 0).to_sql(name = 'taxi_zone_lookup', con = conn, if_exists = 'replace', index = False)

# push the rest of data into table
print(f"populating yellow_tax_table on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
df.to_sql(name = 'yellow_taxi_data', con = conn, if_exists = 'append', index = False)

# push the rest of data into table
print(f"populating taxi_zone_lookup on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
df1.to_sql(name = 'taxi_zone_lookup', con = conn, if_exists = 'append', index = False)

# close connex
print(f"data push complete and closing connection to postgres container on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
conn.close()
