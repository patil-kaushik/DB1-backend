import mysql.connector

CONFIG = {
    "user": "oxg7237_ahc4860",
    "password": "Ahc@4860",
    "host": "51.81.160.154",
    "database": "oxg7237_ahc4860",
}

# CONFIG = {
#     "user": "root",
#     "password": "karannanda95",
#     "host": "localhost",
#     "database": "birdview",
# }

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