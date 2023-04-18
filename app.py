from flask import Flask, request, json
from flask_cors import CORS
from cart import add_cart_item, get_cart_items, remove_cart_item
from db import create_db_connection
from http_codes import http_200, http_500, http_400, http_401
import mysql.connector

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
            query = "SELECT * FROM test_table"
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