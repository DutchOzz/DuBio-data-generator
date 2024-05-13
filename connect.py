import psycopg2
# import sys

# sys.path.append('C:\Users\matie\Documents\Matteo\UT\mod12\code\Autogenerater')

import config

conn = None

def connect():
    try:
        global conn
        conn = psycopg2.connect (
            host = config.hostname, 
            database = config.database, 
            user = config.username, 
            password = config.pwd, 
            port = config.port_id
            )    
    except:
        print("I am unable to connect to the database")

def close():
    conn.close()

connect()
close()