from flask import Flask, request, json
from flask_cors import CORS
from db import create_db_connection
from http_codes import http_200, http_500, http_400, http_401

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/test', methods=['GET'])
def test():
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM CUSTOMER"
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            return http_200("Success!")
        except Exception as e:
            print(e)
        finally:
            if cursor is not None:
                cursor.close()
    except Exception as e:
        print("Database connection failed...\n")
        # print(e)
        return http_500(e)
    finally:
        if connection is not None:
            print("Closing database connection...")
            connection.close()