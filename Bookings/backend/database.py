print("database.py started")
import mysql.connector
from config import DB_CONFIG

def get_connection():

    connection = mysql.connector.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )

    return connection


if __name__ == "__main__":

    try:

        conn = get_connection()

        print("Database Connected Successfully")

        conn.close()

    except Exception as e:

        print("Error:", e)