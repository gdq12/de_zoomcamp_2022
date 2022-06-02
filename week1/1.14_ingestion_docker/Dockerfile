FROM python:3.9.1

RUN pip install pandas sqlalchemy psycopg2 fastparquet

WORKDIR /app
COPY ingest_data.py ingest_data.py

CMD ["python", "ingest_data.py"]
