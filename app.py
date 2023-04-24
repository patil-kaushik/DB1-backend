# Team Members:
# Kaushik Patil - 1001928970
# Vivek Yelethotadahalli Srinivas - 1002064152
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

# @app.route('/itemlist', methods=['GET'])
# def get_item_list():
#     connection = None
#     try:
#         connection = create_db_connection()
#         try:
#             cursor = connection.cursor()
#             query

@app.route('/getitem', methods=['POST'])
def get_item():
    item_name = request.json.get('name')
    iId_value = request.json.get('id')
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            print(item_name)
            cursor.execute(''' SELECT * FROM ITEM WHERE Iname = %s OR iId = %s ''', (item_name,iId_value))
            rows = cursor.fetchall()
            connection.commit()
            data = []
            if rows:
                for row in rows: 
                    resp = {}
                    resp["id"] = row[0]
                    resp["name"] = row[1]
                    resp["price"] = float(row[2])
                    data.append(resp)
            print(data)
            return http_200(data)
        except Exception as e:
            print(e)
        finally:
            if cursor is not None:
                cursor.close()
    except Exception as e:
        print("Database connection failed...\n")
        return http_500(e)
    finally:
        if connection is not None:
            print("Closing database connection...")
            connection.close()

@app.route('/showitems', methods=['GET'])
def show_items():
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(''' SELECT * FROM ITEM ''')
            rows = cursor.fetchall()
            connection.commit()
            data = []
            if rows:
                for row in rows: 
                    resp = {}
                    resp["id"] = row[0]
                    resp["name"] = row[1]
                    resp["price"] = float(row[2])
                    data.append(resp)
            print(data)
            return http_200(data)
        except Exception as e:
            print(e)
        finally:
            if cursor is not None:
                cursor.close()
    except Exception as e:
        print("Database connection failed...\n")
        return http_500(e)
    finally:
        if connection is not None:
            print("Closing database connection...")
            connection.close()

@app.route('/items', methods=['POST'])
def add_item():
    item_name = request.json.get('name')
    iId_value = request.json.get('id')
    price = request.json.get('sprice')
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            print(item_name)
            print(iId_value)
            print(price)
            cursor.execute(''' INSERT INTO ITEM (iId, Iname, Sprice) VALUES(%s,%s,%s)''',(iId_value, item_name, price))
            connection.commit()
            return http_200("Item added successfully")
        except Exception as e:
            print(e)
        finally:
            if cursor is not None:
                cursor.close()
    except Exception as e:
        print("Database connection failed...\n")
        return http_500(e)
    finally:
        if connection is not None:
            print("Closing database connection...")
            connection.close()

@app.route('/updateitem', methods=['POST'])
def update_item():
    item_name = request.json.get('name')
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            print(item_name)
            cursor.execute(''' UPDATE ITEM SET Iname = %s WHERE Iname = %s ''', (item_name, "Carot Sprouts"))
            connection.commit()
            return http_200("Item updated successfully")
        except Exception as e:
            print(e)
        finally:
            if cursor is not None:
                cursor.close()
    except Exception as e:
        print("Database connection failed...\n")
        return http_500(e)
    finally:
        if connection is not None:
            print("Closing database connection...")
            connection.close()

@app.route('/deleteitem', methods=['POST'])
def delete_item():
    item_name = request.json.get('name')
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            print(item_name)
            cursor.execute(''' DELETE FROM ITEM WHERE Iname = %s ''', (item_name,))
            connection.commit()
            return http_200("Item deleted successfully")
        except Exception as e:
            print(e)
        finally:
            if cursor is not None:
                cursor.close()
    except Exception as e:
        print("Database connection failed...\n")
        return http_500(e)
    finally:
        if connection is not None:
            print("Closing database connection...")
            connection.close()