cd C:/Users/toufe/Documents/GitHub/data-engineering-zoomcamp/sandbox/2_docker

docker network create pg_network

docker run \
    --name my_postgresDB \
    --network=pg_network \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v C:/Users/toufe/Documents/GitHub/data-engineering-zoomcamp/sandbox/2_docker/ny_pg_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    -d postgres:13


docker run -p 8080:80 \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="admin" \
  --name my_pgadmin \
  --network=pg_network \
  -d dpage/pgadmin4

python ingest_data.py \
    --username=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --database=ny_taxi \
    --table_name=green_taxi_trips \
    --url="https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-09.parquet"

#buid the docker image
docker build -t taxi_ingest:v001 .

#run the docker image 
#NB: Entrypoint is to the ingest_data.py
docker run -it \
    --network=pg_network \
    taxi_ingest:v001 \
        --username=root \
        --password=root \
        --host=my_postgresDB \
        --port=5432 \
        --database=ny_taxi \
        --table_name=green_taxi_trips \
        --url="https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-09.parquet"

#upload the taxi zone file
docker run -it \
    --network=pg_network \
    taxi_ingest:v001 \
        --username=root \
        --password=root \
        --host=my_postgresDB \
        --port=5432 \
        --database=ny_taxi \
        --table_name=taxi_zone \
        --url="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"
