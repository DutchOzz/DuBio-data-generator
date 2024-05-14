import psycopg2
import config

conn = None

def connect():
    global conn
    conn = psycopg2.connect (
        host = config.hostname, 
        database = config.database, 
        user = config.username, 
        password = config.pwd, 
        port = config.port_id
        )

def close():
    conn.close()

connect()
print("Connected to database")
close()