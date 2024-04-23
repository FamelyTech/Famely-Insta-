import os
import psycopg2
import datetime
import time

conn_params = {'database': 'defaultdb',
               'user': os.getenv('POSTGRES_USER', 'postgres'),
               'password': os.getenv('POSTGRES_PASSWORD', ''),
               'host': os.getenv('POSTGRES_HOST', 'psql-scrapper.c4jc7h3l0yxu.us-east-2.rds.amazonaws.com'),
               'port': os.getenv('POSTGRES_PORT', 25060)}

name = os.getenv('POSTGRES_NAME', 'brattdev')

conn = psycopg2.connect(**conn_params)

conn.set_isolation_level(0)

cur = conn.cursor()

error = True
now = datetime.datetime.now()
deltaT = 0

while error and deltaT < 60:
    deltaT = (datetime.datetime.now() - now).seconds
    try:
        print("Removing active connections")
        cur.execute("""
            select pg_terminate_backend(pid)
            from pg_stat_activity
            where
            datname = '""" + name + """';
        """)
    except Exception as e:
        print(f'Error closing connection: {e}. But we continue')

    try:
        print("Trying to delete:" + name)
        cur.execute("""DROP DATABASE """ + name)
        print("deleted db " + name)
        error = False
    except Exception as e:
        print("Error deleting db but we continue trying")
        print(e)
        time.sleep(5)
    try:
        cur.execute("""CREATE DATABASE """ + name)
        print("created db " + name)
        error = False
    except Exception as e:
        print(e)
        time.sleep(5)
        continue
