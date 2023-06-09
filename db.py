import mysql.connector

CONFIG = {
    "user": "root",
    "password": "",
    "host": "localhost",
    "database": "ArlingtonSprouts",
}

def create_db_connection():
    try:
        connection = mysql.connector.connect(
            user=CONFIG["user"],
            password=CONFIG["password"],
            host=CONFIG["host"],
            database=CONFIG["database"],
        )
        return connection
    except Exception as e:
        print(e)