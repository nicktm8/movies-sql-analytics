import sqlite3

def get_connection():
    conn = sqlite3.connect('db/movies.db')
    return conn
