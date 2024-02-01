# ```
# pip install sqlalchemy psycopg-binary psycopg2-binary pyarrow pandas
# ```

import argparse
import pandas as pd
import datetime
from time import time
from sqlalchemy import create_engine
import requests
import pyarrow.parquet as pq


#-------------------------------------------------------------------------
#function section

def download_file(url, filename=None):
    """Downloads a file from a URL and saves it to disk.

    Args:
        url (str): The URL of the file to download.
        filename (str, optional): The desired filename to save the file as.
            If not provided, the filename will be extracted from the URL.

    Returns:
        str: The path to the downloaded file.

    Example usage:
        url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-09.parquet"
        downloaded_file = download_file(url)
        print(f"Downloaded file to: {downloaded_file}")
    """

    response = requests.get(url, stream=True)

    # Handle potential errors
    response.raise_for_status()  # Raise an exception for non-200 status codes

    if filename is None:
        filename = url.split("/")[-1]  # Extract filename from URL if not provided

    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:  # Filter out keep-alive new chunks
                f.write(chunk)

    return filename

def csv_insgest(params):

    #need script to download file
    csv_name = 'ingest_data.csv'
    download_file(params.url, csv_name)

    #-------------------------------------------------------------------------
    #create connection to database    
    engine = create_engine(f'postgresql://{params.username}:{params.password}@{params.host}:{params.port}/{params.database}')
    engine.connect()

    table_name = params.table_name
    #drop table if exists
    #engine.execute("DROP TABLE IF EXISTS %s;" % table_name)

    #show time started
    print("Started: %s" % datetime.datetime.now())

    #reading in CSV
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000, low_memory=False)
    for batch in df_iter:
        t_start = time()
        
        df = batch
        df.to_sql(name=table_name, con=engine, if_exists="append")
        
        t_end = time()  
        print("New chunk inserted: %.3f elapsed" % (t_end - t_start))

    print("Ended: %s" % datetime.datetime.now())

def parquet_ingest(params):
    #need script to download file
    parquet_filename = 'ingest_data.parquet'
    download_file(params.url, parquet_filename)

    #-------------------------------------------------------------------------
    #create connection to database    
    engine = create_engine(f'postgresql://{params.username}:{params.password}@{params.host}:{params.port}/{params.database}')
    engine.connect()

    table_name = params.table_name
    #drop table if exists
    #engine.execute("DROP TABLE IF EXISTS %s;" % table_name)

    #show time started
    print("Started: %s" % datetime.datetime.now())

    #reading in parquet
    parquet_file = pq.ParquetFile(parquet_filename)
    for batch in parquet_file.iter_batches(batch_size=100000):
        t_start = time()
        
        df = batch.to_pandas()
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
        df.to_sql(name=table_name, con=engine, if_exists="append")
        
        t_end = time()  
        print("New chunk inserted: %.3f elapsed" % (t_end - t_start))
        
    print("Ended: %s" % datetime.datetime.now())

#-------------------------------------------------------------------------
#main executions section
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingerst CSV into Postgres DB')

    parser.add_argument('--username'  , help='username for postgres')       
    parser.add_argument('--password'  , help='password for postgres')
    parser.add_argument('--host'      , help='host for postgres')
    parser.add_argument('--port'      , help='port for postgres')
    parser.add_argument('--database'  , help='database for postgres')
    parser.add_argument('--table_name', help='table name for postgres')
    parser.add_argument('--url'       , help='csv_url to ingest')

    args = parser.parse_args()
    ext = args.url.split(".")[-1]
    print(ext)

    if ext == 'parquet': parquet_ingest(args)
    if ext =='csv': csv_insgest(args)