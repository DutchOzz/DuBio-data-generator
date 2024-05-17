import psycopg2
import config

# Establish a connection to the database
def connect():
    conn = psycopg2.connect (
        host = config.hostname, 
        database = config.database, 
        user = config.username, 
        password = config.pwd, 
        port = config.port_id
        )
    return conn

# Close the connection to the database
def close(conn):
    conn.close()