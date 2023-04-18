import json
from db import create_db_connection
from http_codes import http_200, http_404, http_500


def add_cart_item(user, product):
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            existing_cart_query = f"SELECT * FROM CART WHERE customer_id = {user['user_id']}"
            cursor.execute(existing_cart_query)
            existing_cart_row = cursor.fetchone()
            if existing_cart_row:
                existing_cart = json.loads(existing_cart_row[4])
                existing_cart.append(product['id'])
                add_item_query = f"UPDATE CART SET products='{json.dumps(existing_cart)}' WHERE id={existing_cart_row[0]}"
                cursor.execute(add_item_query)
            else:
                products = []
                products.append(product['id'])
                create_cart_query = f"INSERT INTO CART(customer_id, products) VALUES({user['user_id']}, '{json.dumps(products)}')"
                cursor.execute(create_cart_query)
            connection.commit()
            return http_200("Success")
        except Exception as e:
            print(e)
            return http_500(e)
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

def get_cart_items(user):
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            query = f"SELECT * FROM CART WHERE customer_id = {user['user_id']}"
            cursor.execute(query)
            row = cursor.fetchone()
            if row:
                products_ids = json.loads(row[4])
                products = []
                for id in products_ids:
                    product_query = f"SELECT * FROM PRODUCTS WHERE id={id}"
                    cursor.execute(product_query)
                    row = cursor.fetchone()
                    product = {}
                    product['id'] = row[0]
                    product['name'] = row[1]
                    product['images'] = json.loads(row[2])
                    product['price'] = row[10] 
                    products.append(product)
                return http_200(products)
            return http_200([])
        except Exception as e:
            print(e)
            return http_500(e)
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

def remove_cart_item(user, product):
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            existing_cart_query = f"SELECT * FROM CART WHERE customer_id = {user['user_id']}"
            cursor.execute(existing_cart_query)
            existing_cart_row = cursor.fetchone()
            if existing_cart_row:
                existing_cart = json.loads(existing_cart_row[4])
                for item in existing_cart:
                    if item == product['id']:
                        existing_cart.remove(product['id'])
                add_item_query = f"UPDATE CART SET products='{json.dumps(existing_cart)}' WHERE id={existing_cart_row[0]}"
                cursor.execute(add_item_query)
                connection.commit()
                return http_200("Success")
            return http_404("Cart not found")
        except Exception as e:
            print(e)
            return http_500(e)
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