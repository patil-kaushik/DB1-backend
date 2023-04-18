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


@app.route('/categories', methods=['GET'])
def get_categories():
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM SERVICE_CATEGORY"
            cursor.execute(query)
            rows = cursor.fetchall()
            data = []
            if rows:
                for row in rows:
                    d = {}
                    d["name"] = row[1]
                    d["code"] = row[2]
                    data.append(d)
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


@app.route('/users/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data['email']
    password = data['password']

    connection = None

    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                'SELECT * FROM USERS WHERE email = %s AND password = %s', (email, password,))
            user = cursor.fetchone()

            if user:
                data = {"status": "success", "user_id": user[0], "user_type": user[1], "account_status": user[2],
                        "email": user[3]}
                return http_200(data)
            else:
                return http_401("Invalid email or password")
        except Exception as e:
            print(e)
            return http_400(e)
        finally:
            if cursor is not None:
                cursor.close()
    except Exception as e:
        print("Error...\n")
        return http_500(e)
    finally:
        if connection is not None:
            print("Closing database connection...")
            connection.close()


@app.route('/users/register', methods=['POST'])
def register_user():
    data = request.get_json()
    user_type = data['user_type']
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    password = data['password']
    phone = data['phone']
    dob = data['dob']
    street = data['street']
    city = data['city']
    zipcode = data['zipcode']
    state = data['state']
    country = data['country']
    account_status = 0

    if user_type == 1:
        account_status = 1

    connection = None

    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(''' INSERT INTO USERS (user_type,account_status, email, first_name, last_name, password, phone, dob, 
                            street, city, zipcode, state, country) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                           (user_type, account_status, email, first_name, last_name, password, phone, dob, street, city,
                            zipcode, state, country))
            connection.commit()

            return http_200({"status": "success"})
        except mysql.connector.errors.IntegrityError as e:
            print(e)
            if e.errno == 1062:
                return http_400("Email already registered. Please register with a different email address.")
            return http_400(e.msg)
        finally:
            if cursor is not None:
                cursor.close()
    except Exception as e:
        print("Error...\n")
        return http_500(e)
    finally:
        if connection is not None:
            print("Closing database connection...")
            connection.close()


@app.route('/users/profile', methods=['POST'])
def user_profile():
    data = request.get_json()
    user_id = data['id']

    connection = None

    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()

            cursor.execute('SELECT * FROM USERS WHERE id = %s', (user_id,))

            user = cursor.fetchone()

            if user:
                data = {"user_id": user[0], "user_type": user[1], "account_status": user[2], "email": user[3],
                        "first_name": user[4],
                        "last_name": user[5], "phone": user[7], "dob": str(user[8]), "street": user[9],
                        "city": user[10], "zipcode": user[11], "state": user[12], "country": user[13]}
                return http_200(data)
            else:
                return http_400("Invalid User Id")
        except Exception as e:
            print(e)
            return http_400(e)
        finally:
            if cursor is not None:
                cursor.close()
    except Exception as e:
        print("Error...\n")
        return http_500(e)
    finally:
        if connection is not None:
            print("Closing database connection...")
            connection.close()


@app.route('/users/vendors', methods=['GET'])
def user_vendors():
    connection = None

    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()

            cursor.execute('SELECT * FROM users WHERE user_type = 2')

            rows = cursor.fetchall()
            data = []
            if rows:
                for user in rows:
                    print(user)
                    data.append({"user_id": user[0], "user_type": user[1], "account_status": user[2], "email": user[3],
                                 "first_name": user[4],
                                 "last_name": user[5], "phone": user[7], "dob": str(user[8]), "street": user[9],
                                 "city": user[10], "zipcode": user[11], "state": user[12], "country": user[13]})
            return http_200(data)
        except Exception as e:
            print(e)
            return http_400(e)
        finally:
            if cursor is not None:
                cursor.close()
    except Exception as e:
        print("Error...\n")
        return http_500(e)
    finally:
        if connection is not None:
            print("Closing database connection...")
            connection.close()


@app.route('/users/vendors', methods=['PUT'])
def users_vendors_update():
    data = request.get_json()
    user_id = data['user_id']
    account_status = data['account_status']

    connection = None

    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                ' UPDATE USERS SET account_status = %s WHERE id = %s', (account_status, user_id,))
            connection.commit()

            return http_200({"status": "success"})
        except mysql.connector.errors.IntegrityError as e:
            print(e)
            return http_400(e.msg)
        finally:
            if cursor is not None:
                cursor.close()
    except Exception as e:
        print("Error...\n")
        return http_500(e)
    finally:
        if connection is not None:
            print("Closing database connection...")
            connection.close()


@app.route('/products', methods=['GET'])
def get_products():
    id = request.args.get('id')
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            if not id:
                cursor.execute("SELECT * FROM PRODUCTS")
            else:
                cursor.execute('SELECT * FROM PRODUCTS WHERE id = %s', (id,))
            products = cursor.fetchall()
            data = []
            if products:
                for product in products:
                    images_object = json.loads(str(product[2]))

                    # request_object = json.loads(str(product[5]))

                    offer_object = json.loads(str(product[9]))

                    data.append({"id": product[0],
                                 "name": product[1],
                                 "images": images_object,
                                 "description": product[3],
                                 "condition": product[4],
                                 # "requested_by": request_object,
                                 "available_quantity": product[5],
                                 "availability": product[6],
                                 "category": product[7],
                                 "seller_Id": product[8],
                                 "offer": offer_object,
                                 "price": product[10]
                                 })
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


@app.route('/products/<int:product_id>', methods=['GET'])
def getProduct(product_id):
    print(product_id)
    connection = None
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM PRODUCTS WHERE id = %s', (product_id,))
        prod = cursor.fetchone()

        images_object = json.loads(str(prod[2]))
        offer_object = json.loads(str(prod[9]))
        requested_prod = {
            "id": prod[0],
            "name": prod[1],
            "images": images_object,
            "description": prod[3],
            "condition": prod[4],
            "available_quantity": prod[5],
            "availability": prod[6],
            "category": prod[7],
            "seller_Id": prod[8],
            "offer": offer_object,
            "price": prod[10]
        }

        try:
            cursor = connection.cursor()
            return http_200(requested_prod)
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


@app.route('/products/update', methods=['PUT'])
def update():
    updateData = request.get_json()

    print(updateData)
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            # return http_200("Success")
            try:
                availability = updateData.get('availability')
                available_quantity = updateData.get('available_quantity')
                category = updateData.get('category')
                condition = updateData.get('condition')
                description = updateData.get('description')
                images = json.dumps(updateData.get('images'))
                name = updateData.get('name')
                offer = json.dumps(updateData.get('offer'))
                seller_Id = updateData.get('seller_Id')
                price = updateData.get('price')
                prod_id = updateData.get('id')

                if prod_id:
                    cursor.execute("UPDATE PRODUCTS SET name=%s, description=%s, price=%s, availability=%s, available_quantity=%s, category=%s,offer=%s, images=%s WHERE id=%s",
                                   (name, description, price, availability, available_quantity, category, offer, images, prod_id, ))
                    connection.commit()
                    return http_200('Product updated successfully!')
                else:
                    cursor.execute('''INSERT INTO PRODUCTS (name, description, price, availability, available_quantity, category, seller_id, offer, images) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                                   (name, description, price, availability, available_quantity, category, seller_Id, offer, images, ))
                    connection.commit()
                    return http_200('Product created successfully!')

            except AssertionError as e:
                # if an AssertionError is raised, return a 400 response with the error message
                return http_400(str(e))
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


@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    updateData = request.get_json()

    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            try:
                availability = updateData.get('availability')
                available_quantity = updateData.get('available_quantity')
                category = updateData.get('category')
                condition = updateData.get('condition')
                description = updateData.get('description')
                images = updateData.get('images')
                name = updateData.get('name')
                offer = updateData.get('offer')
                requested_by = updateData.get('requested_by')
                seller_Id = updateData.get('seller_Id')

                query = 'UPDATE PRODUCTS SET '
                params = []
                if availability:
                    assert isinstance(
                        availability, str), "availability must be a string"
                    assert (
                        availability == "InStock" or availability == "OutOfStock"), "availability can either be 'InStock' or 'OutOfStock'"
                    query += 'availability=%s, '
                    params.append(availability)
                if available_quantity is not None:
                    assert isinstance(
                        available_quantity, int), "available_quantity must be an integer"
                    assert (available_quantity >=
                            0), "available_quantity should be greater than 0"
                    query += 'available_quantity=%s, '
                    params.append(available_quantity)
                if category:
                    assert isinstance(
                        category, str), "category must be a string"
                    query += 'category=%s, '
                    params.append(category)
                if condition:
                    assert isinstance(
                        condition, str), "condition must be a string"
                    assert (condition >=
                            0), "availability can either be 'New' or 'Used'"
                    query += 'condition=%s, '
                    params.append(condition)
                if description:
                    assert isinstance(
                        description, str), "description must be a string"
                    query += 'description=%s, '
                    params.append(description)
                if images:
                    # assert isinstance(images, [str]), "images must be an array of string"
                    query += 'images=%s, '
                    params.append(json.dumps(images))
                if name:
                    assert isinstance(name, str), "name must be a string"
                    query += 'name=%s, '
                    params.append(name)
                if offer:
                    assert (isinstance(offer['offerPrice'], int) or isinstance(offer['offerPrice'],
                                                                               float)), "offerPrice must be numeric"
                    assert (isinstance(offer['originalPrice'], int) or isinstance(offer['originalPrice'],
                                                                                  float)), "originalPrice must be numeric"
                    assert (float(offer['offerPrice']) <= float(
                        offer['originalPrice'])), "offerPrice cannot be more than originalPrice"
                    assert (offer['type'] == "Offer" or offer['type']
                            == "None"), "type can either be 'Offer' or 'None'"
                    query += 'offer=%s, '
                    params.append(json.dumps(offer))
                if requested_by:
                    # assert isinstance(requested_by['quantity'], int), "quantity must be an integer"
                    # assert (requested_by['quantity'] > 0), "quantity must be greater than 0"
                    # assert isinstance(requested_by['user_id'], int), "user_id must be an integer"
                    query += 'requested_by=%s, '
                    params.append(json.dumps(requested_by))
                if seller_Id:
                    query += 'seller_Id=%s, '
                    params.append(seller_Id)

                query = query[:-2]

                query += ' WHERE id=%s'
                print("query is ", query)
                params.append(product_id)
                print("params are ", tuple(params))

                cursor.execute(query, tuple(params))
                connection.commit()
                return http_200('Product updated successfully!')
            except AssertionError as e:
                # if an AssertionError is raised, return a 400 response with the error message
                return http_400(str(e))
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


@app.route('/products/requests', methods=['GET'])
def product_request():
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM PRODUCT_REQUESTS"
            cursor.execute(query)
            rows = cursor.fetchall()
            data = []
            if rows:
                for row in rows:
                    cursor.execute(
                        'SELECT * FROM PRODUCTS WHERE id = %s', (row[1],))
                    prod = cursor.fetchone()

                    images_object = json.loads(str(prod[2]))
                    offer_object = json.loads(str(prod[9]))
                    requested_prod = {
                        "id": prod[0],
                        "name": prod[1],
                        "images": images_object,
                        "description": prod[3],
                        "condition": prod[4],
                        "available_quantity": prod[5],
                        "availability": prod[6],
                        "category": prod[7],
                        "seller_Id": prod[8],
                        "offer": offer_object
                    }

                    cursor.execute(
                        'SELECT * FROM USERS WHERE id = %s', (row[2],))
                    user = cursor.fetchone()
                    requested_by = {}
                    if user:
                        requested_by = {
                            "user_id": user[0], "user_type": user[1], "account_status": user[2], "email": user[3],
                            "first_name": user[4],
                            "last_name": user[5], "phone": user[7], "dob": str(user[8]), "street": user[9],
                            "city": user[10], "zipcode": user[11], "state": user[12], "country": user[13]
                        }
                    data.append(
                        {"id": row[0], "product": requested_prod, "requested_by": requested_by, "filled": row[3],
                         "quantity": row[6]})
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


@app.route('/products/requests/fill', methods=['PUT'])
def product_requests_fill():
    data = request.get_json()
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE PRODUCT_REQUESTS SET filled=%s  WHERE id = %s", (1, data.get('req_id'),))

            cursor.execute('SELECT * FROM PRODUCTS WHERE id = %s',
                           (data.get('prod_id'),))
            prod = cursor.fetchone()

            updated_qty = int(prod[5] + data.get('quantity'))
            cursor.execute("UPDATE PRODUCTS SET available_quantity=%s WHERE id = %s",
                           (updated_qty, data.get('prod_id'),))
            connection.commit()
            return http_200("Success")
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


@app.route('/products/requests/<int:product_id>', methods=['PUT'])
def product_requests(product_id):
    data = request.get_json()
    print(data)
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE PRODUCT_REQUESTS SET filled=%s WHERE prod_id = %s", (1, product_id,))

            cursor.execute(
                'SELECT * FROM PRODUCTS WHERE id = %s', (product_id,))
            prod = cursor.fetchone()

            updated_qty = int(prod[5] + data.get('quantity'))
            cursor.execute(
                "UPDATE PRODUCTS SET available_quantity=%s WHERE id = %s", (updated_qty, product_id,))
            connection.commit()
            return http_200("Success")
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


@app.route('/service-request', methods=['PUT'])
def create_service_request():
    args = request.get_json()
    customer_id = args['customerID']
    service_category_code = str(args['serviceCategoryCode'])
    date_time = str(args['dateTime'])
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            query = f'INSERT INTO SERVICE_REQUEST(service_category_code, customer_id, requested_on) VALUES("{service_category_code}", {customer_id}, "{date_time}")'
            print(query)
            cursor.execute(query)
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


@app.route('/cart/add', methods=['PUT'])
def add_item():
    args = request.get_json()
    user = args['user']
    product = args['product']
    res = add_cart_item(user, product)
    return res


@app.route('/cart/get', methods=['POST'])
def get_cart():
    args = request.get_json()
    user = args['user']
    res = get_cart_items(user)
    return res


@app.route('/cart/remove', methods=['PUT'])
def remove_item():
    args = request.get_json()
    user = args['user']
    product = args['product']
    res = remove_cart_item(user, product)
    return res


@app.route('/service-request/update/<int:request_id>', methods=['PUT'])
def update_service_request(request_id):
    args = request.get_json()
    requested_on = args['requested_on']
    updated_datetime = args['updated_datetime']
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE SERVICE_REQUEST SET updated_on=%s,requested_on=%s  WHERE id = %s",
                           (updated_datetime, requested_on, request_id,))
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


@app.route('/service-request/status-update/<int:request_id>', methods=['PUT'])
def status_update_service_request(request_id):
    args = request.get_json()
    request_status = args['request_status']  # 0-default, 1-accept, 2-reject
    updated_datetime = args['updated_datetime']
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE SERVICE_REQUEST SET request_status=%s,updated_on=%s,completed_on=%s  WHERE id = %s",
                           (request_status, updated_datetime, updated_datetime, request_id,))
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


@app.route('/service-request', methods=['GET'])
def service_request():
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM SERVICE_REQUEST"
            cursor.execute(query)
            rows = cursor.fetchall()
            data = []
            if rows:
                for request in rows:
                    print(request)
                    cursor.execute(
                        'SELECT * FROM USERS WHERE id = %s', (request[2],))
                    user = cursor.fetchone()
                    obj = {"id": request[0], "service_category_code": request[1], "customer_id": request[2], "vendor_id": request[3],
                           "created_on": str(request[4]),
                           "updated_on": str(request[5]), "requested_on": str(request[6]), "completed_on": str(request[7]), "payment_status": request[8],
                           "request_status": request[9]}
                    if user:
                        customer = {
                            "user_id": user[0], "user_type": user[1], "account_status": user[2], "email": user[3],
                            "first_name": user[4],
                            "last_name": user[5], "phone": user[7], "dob": str(user[8]), "street": user[9],
                            "city": user[10], "zipcode": user[11], "state": user[12], "country": user[13]
                        }
                        obj["customer"] = customer
                    data.append(obj)
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


@app.route('/service-request/<int:customer_id>', methods=['GET'])
def service_request_customer(customer_id):
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM SERVICE_REQUEST WHERE customer_id=%s", (customer_id,))
            rows = cursor.fetchall()
            data = []
            if rows:
                for request in rows:
                    print(request)
                    data.append({"id": request[0], "service_category_code": request[1], "customer_id": request[2], "vendor_id": request[3],
                                 "created_on": str(request[4]),
                                 "updated_on": str(request[5]), "requested_on": str(request[6]), "completed_on": str(request[7]), "payment_status": request[8],
                                 "request_status": request[9]})
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


@app.route('/orders/customer/<int:customer_id>', methods=['GET'])
def orders_customer(customer_id):
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM PAYMENTS WHERE user_id = %s', (customer_id,))
            rows = cursor.fetchall()
            data = []
            if rows:
                for item in rows:
                    obj = {"id": item[0], "customer_id": item[1],
                           "total_price": item[6], "transaction_id": item[7],
                           "timestamp": str(item[3]), "payment_method": item[10], "card_number": item[11]}

                    products = []
                    for product in json.loads(item[5].replace("'", "\"")):
                        cursor.execute(
                            'SELECT * FROM PRODUCTS WHERE id = %s', (product,))
                        res1 = cursor.fetchone()
                        if res1:
                            product_obj = {"id": res1[0], "name": res1[1], "price": res1[10], "seller_id": res1[8]}
                            products.append(product_obj)

                    obj["products"] = products
                    data.append(obj)

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


@app.route('/orders/vendor/<int:seller_id>', methods=['GET'])
def orders_vendor(seller_id):
    connection = None
    try:
        connection = create_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM PAYMENTS')
            rows = cursor.fetchall()
            data = []
            if rows:
                for item in rows:
                    print(item)

                    products = []
                    for product in json.loads(item[5].replace("'", "\"")):
                        cursor.execute(
                            'SELECT * FROM PRODUCTS WHERE id = %s', (product,))
                        res1 = cursor.fetchone()
                        if res1:
                            if str(res1[8]) == str(seller_id):
                                product_obj = {"id": res1[0], "name": res1[1], "price": res1[10]}
                                products.append(product_obj)

                    if len(products) > 0:
                        cursor.execute(
                            'SELECT * FROM USERS WHERE id = %s', (item[1],))
                        res2 = cursor.fetchone()
                        if res2:
                            customer_obj = {"id": res2[0], "name": res2[4]+" "+res2[5],
                                            "email": res2[3], "phone": res2[7],
                                            "address": res2[9] + ", " + res2[10] + ", " + res2[12] + ", " + res2[11]}

                        obj = {"id": item[0], "customer": customer_obj, "seller_id": seller_id, "total_price": item[6],
                               "transaction_id": item[7], "timestamp": str(item[3]), "payment_method": item[10],
                               "card_number": item[11], "products": products}

                        data.append(obj)

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