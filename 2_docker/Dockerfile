FROM python:3.9.1

RUN pip install requests sqlalchemy psycopg2 psycopg psycopg-binary psycopg2-binary pyarrow pandas

WORKDIR /app
COPY ingest_data.py ingest_data.py

ENTRYPOINT [ "python","ingest_data.py" ]