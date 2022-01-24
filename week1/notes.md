### Docker

Good to know in the command line:

* to run the image interactively use `-it` flag

```
docker run -it ubuntu bash

# ubuntu - image name
# bash - program/command to run once enter container
```

* to enter an image's specific entry point (aka program) that the image is build off of

```
docker run -it --entrypoint=bash python:3.9

# enter python container in bash mode so can pip install necessary packages etc.
```

* to run docker container with a specific variable needed by the script

```
docker run -it test:pandas 2021-01-01

# 2021-01-01 variable required for the script in the container to run successfully
```

* python command to assign external input to a variable in its environment

```
import sys

sys.arv[0] # assigned to the name of the script always

sys.arv[1] # name of 1 or more variables fed to the script
```

Dockerfiles:

* structure:

```
# indicate which image want to pull
FROM python:3.9

# commands to run once inside the container
RUN pip install pandas

# create the directory in which the container will cd into
WORKDIR /app

# copy files from local directory to image/container (in /app directory)
COPY localFile.py destinationFile.py

# which program should the container start with once it enters and run which script
ENTRYPOINT ["python", "destinationFile.py"]
```

* command to build container based on docker file (command must be executed in the directory of the docker file)

```
docker build -t test::pandas .

# test is the image name to be assigned
# pandas in this case is the tag to image, this is usually a version number
```

## Postgres in Docker

* pull postgres image and create container

```
docker run -it -p 5432:5432 -e POSTGRES_USER=root -e POSTGRES_PASSWORD=root -e POSTGRES_DB=ny_taxi -v $(pwd)/data_folder:/var/lib/postgresql/data postgres:13

# -e is assign necessary environment variables within container
# -v to map/mounting info into container like data or credentials
```

* client to access postgres in container

```
# install python base package on local machine
pip install pgcli

# access pgcli locally
pgcli -h localhost -p 5432 -u root -d dbName
```

* good to know commands for pgcli

```
# list of data bases
\dt

# to describe a table in schema
\d dbTable
```

* exploring and loading data via python. [Webpage](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page) to find all data, yellow taxi [data set doc](https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf)

```
# necessary libraries
import pandas as pd
from sqlalchemy import create_engine
from time import time

# download nyc dataset locally
!wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv

# load data into python environment
df_iter = pd.read_csv('yellow_tripdata_2021-01.csv', iterator = True, chunksize = 10.000)

# to fetch only 1 chunk of df into python
df = df_iter.next()

# convert certain columns in df to correct data type of exportation
df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

# connect to db
engine = creat_engine('postgresql://root:root@localhost:5432/ny_taxi')
engine.connect()

# generate string variable for create table command (in DDL language)
create_query = pd.io.sql.get_schema(df, 'yellow_taxi_data', con = engine)

# push data to database
while True:
  t1 = time()
  # fetch chunk from df iterator
  df = df_iter.next()
  # convert columns to necessary data types
  df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
  df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
  # push data to postgres
  df.to_sql(name = 'yellow_taxi_data', con = engine, if_exists = 'append')
  t2 = time()
  print(f"push {df.shape[0]} records int yellow_taxi_data postgres table in {round(t2 - t1, 2)} seconds")
```

## pdAdmin Docker

* pull image and create container

```
docker run -it -e POSTGRES_USER=root -e POSTGRES_PASSWORD=root -e POSTGRES_DB=ny_taxi -p 8080:80 dpage/pdadmin4

# then go to following link in browser
localhost:8080

# once enter pgAdmin must create a server and enter the same credentials used to create the container
```

* connex container to postgres by creating a network

```
# define the network
docker network create pg-network

# link the containers back to the network (postgres db container)
docker run -it -p 5432:5432 -e POSTGRES_USER=root -e POSTGRES_PASSWORD=root -e POSTGRES_DB=ny_taxi -v $(pwd)/data_folder:/var/lib/postgresql/data --network=pg-network --name pg-databse postgres:13

# link pgAdmin container to network
docker run -it -e POSTGRES_USER=root -e POSTGRES_PASSWORD=root -e POSTGRES_DB=ny_taxi -p 8080:80 --network=pg-network --name pdadmin dpage/pdadmin4


# then go to following link in browser
localhost:8080

# once enter pgAdmin must create a server and enter the same credentials used to create the container
# hostname will be the name variable assigned to the postgres docker
```

#3 Docker Compose
