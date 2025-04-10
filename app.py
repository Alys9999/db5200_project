import os
import uuid
import mysql.connector
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)


def get_db_connection():
    # return mysql.connector.connect(
    #     host=os.environ.get("MYSQL_HOST"),
    #     user=os.environ.get("MYSQL_USER"),
    #     password=os.environ.get("MYSQL_PASSWORD"),
    #     database=os.environ.get("MYSQL_DATABASE")
    # )

    return mysql.connector.connect(
        host = "35.209.13.18",
        user = "g41v1rj",
        password = "000000",
        database = "neushop"
    )



# 1. Show all products in a given category with a price below a given threshold.
@app.route('/products/<category>/<float:max_price>', methods=['GET'])
def get_products_by_category_and_price(category, max_price):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT p.*
    FROM PRODUCT p
    JOIN CATEGORY c ON p.category_id = c.category_id
    WHERE c.category_name = %s
      AND p.price < %s;
    """
    cursor.execute(query, (category, max_price))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(products)


# 2. List the top best selling products in the last N days, limited to a specified number.
@app.route('/products/best-selling/<int:days>/<int:limit>', methods=['GET'])
def get_best_selling_products(days, limit):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # Using f-string formatting for INTERVAL and LIMIT (safe since days and limit are integers)
    query = f"""
    SELECT p.product_id, p.name, SUM(oi.quantity) AS total_sold
    FROM PRODUCT p
    JOIN ORDERITEM oi ON p.product_id = oi.product_id
    JOIN `ORDER` o ON oi.order_id = o.order_id
    WHERE o.order_date >= DATE_SUB(NOW(), INTERVAL {days} DAY)
    GROUP BY p.product_id, p.name
    ORDER BY total_sold DESC
    LIMIT {limit};
    """
    cursor.execute(query)
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(products)

# 3. Display all orders placed by a given customer in the past N days.
@app.route('/orders/customer/<customer_id>/<int:days>', methods=['GET'])
def get_orders_by_customer(customer_id, days):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = f"""
    SELECT *
    FROM `ORDER`
    WHERE user_id = %s
      AND order_date >= DATE_SUB(NOW(), INTERVAL {days} DAY);
    """
    cursor.execute(query, (customer_id,))
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(orders)

# 4. Get the current inventory status for a product by its SKU.
@app.route('/product/inventory/<product_id>', methods=['GET'])
def get_product_inventory(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT product_id, name, stock_quantity
    FROM PRODUCT
    WHERE product_id = %s;
    """
    cursor.execute(query, (product_id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(product)

# 5. Show all customers who have spent over a given amount in total purchases.
@app.route('/customers/high-spenders/<float:min_spent>', methods=['GET'])
def get_high_spending_customers(min_spent):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT o.user_id, SUM(o.total_amount) AS total_spent
    FROM `ORDER` o
    GROUP BY o.user_id
    HAVING total_spent > %s;
    """
    cursor.execute(query, (min_spent,))
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(customers)

# 6. List all products with less than a specified number of items in stock.
@app.route('/products/low-stock/<int:threshold>', methods=['GET'])
def get_low_stock_products(threshold):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT *
    FROM PRODUCT
    WHERE stock_quantity < %s;
    """
    cursor.execute(query, (threshold,))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(products)

# 8. Display all orders that are currently marked with a specified status.
@app.route('/orders/status/<status>', methods=['GET'])
def get_orders_by_status(status):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT *
    FROM `ORDER`
    WHERE status = %s;
    """
    cursor.execute(query, (status,))
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(orders)

# 9. Show the total revenue generated in the last N days.
@app.route('/revenue/<int:days>', methods=['GET'])
def get_revenue(days):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = f"""
    SELECT SUM(total_amount) AS total_revenue
    FROM `ORDER`
    WHERE order_date >= DATE_SUB(NOW(), INTERVAL {days} DAY);
    """
    cursor.execute(query)
    revenue = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(revenue)



# Table metadata for allowed tables.
# Only tables with a single primary key are supported by this generic CRUD.
TABLE_METADATA = {
    "USER": {
        "primary_key": "user_id",
        "columns": ["user_id", "username", "password", "email", "created_at"],
        "insertable": ["user_id", "username", "password", "email"]
    },
    "CUSTOMER": {
        "primary_key": "user_id",
        "columns": ["user_id", "first_name", "last_name", "phone"],
        "insertable": ["user_id", "first_name", "last_name", "phone"]
    },
    "SELLER": {
        "primary_key": "user_id",
        "columns": ["user_id", "store_name", "business_license"],
        "insertable": ["user_id", "store_name", "business_license"]
    },
    "ADMIN": {
        "primary_key": "user_id",
        "columns": ["user_id", "admin_level"],
        "insertable": ["user_id", "admin_level"]
    },
    "CATEGORY": {
        "primary_key": "category_id",
        "columns": ["category_id", "category_name", "description"],
        "insertable": ["category_id", "category_name", "description"]
    },
    "CART": {
        "primary_key": "cart_id",
        "columns": ["cart_id", "created_at", "user_id"],
        "insertable": ["cart_id", "user_id"]
    },
    "PRODUCT": {
        "primary_key": "product_id",
        "columns": ["product_id", "name", "price", "description", "stock_quantity", "created_at", "user_id", "category_id"],
        "insertable": ["product_id", "name", "price", "description", "stock_quantity", "user_id", "category_id"]
    },
    "ORDER": {
        "primary_key": "order_id",
        "columns": ["order_id", "order_date", "status", "total_amount", "user_id"],
        "insertable": ["order_id", "status", "total_amount", "user_id"]
    },
    "ORDERITEM": {
        "primary_key": "order_item_id",
        "columns": ["order_item_id", "quantity", "item_price", "order_id", "product_id"],
        "insertable": ["order_item_id", "quantity", "item_price", "order_id", "product_id"]
    },
    "PAYMENT": {
        "primary_key": "payment_id",
        "columns": ["payment_id", "payment_date", "payment_amount", "payment_method"],
        "insertable": ["payment_id", "payment_amount", "payment_method"]
    }
}

def get_table_metadata(table_name):
    return TABLE_METADATA.get(table_name.upper())

# GET all records from a given table.
@app.route('/<table>', methods=['GET'])
def get_all_records(table):
    meta = get_table_metadata(table)
    if not meta:
        return jsonify({"error": "Invalid table"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql = f"SELECT * FROM {table.upper()}"
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

# GET a single record by primary key.
@app.route('/<table>/<pk>', methods=['GET'])
def get_record(table, pk):
    meta = get_table_metadata(table)
    if not meta or not meta.get("primary_key"):
        return jsonify({"error": "Invalid table or composite primary key not supported"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    pk_column = meta["primary_key"]
    sql = f"SELECT * FROM {table.upper()} WHERE {pk_column} = %s"
    cursor.execute(sql, (pk,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return jsonify(row)
    else:
        return jsonify({"error": "Record not found"}), 404

# POST: Create a new record in a given table.
@app.route('/<table>', methods=['POST'])
def create_record(table):
    meta = get_table_metadata(table)
    if not meta:
        return jsonify({"error": "Invalid table"}), 400
    data = request.json
    # Only use columns allowed for insert
    insertable = meta.get("insertable", [])
    insert_data = {col: data[col] for col in insertable if col in data}
    if not insert_data:
        return jsonify({"error": "No valid data provided"}), 400
    cols = ", ".join(insert_data.keys())
    placeholders = ", ".join(["%s"] * len(insert_data))
    sql = f"INSERT INTO {table.upper()} ({cols}) VALUES ({placeholders})"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, tuple(insert_data.values()))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"message": "Record created"}), 201

# PUT: Update an existing record in a given table.
@app.route('/<table>/<pk>', methods=['PUT'])
def update_record(table, pk):
    meta = get_table_metadata(table)
    if not meta or not meta.get("primary_key"):
        return jsonify({"error": "Invalid table or composite primary key not supported"}), 400
    data = request.json
    allowed_columns = meta.get("columns", [])
    # Exclude the primary key from being updated.
    update_data = {col: data[col] for col in allowed_columns if col in data and col != meta["primary_key"]}
    if not update_data:
        return jsonify({"error": "No valid data provided for update"}), 400
    set_clause = ", ".join([f"{col}=%s" for col in update_data])
    sql = f"UPDATE {table.upper()} SET {set_clause} WHERE {meta['primary_key']} = %s"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, tuple(update_data.values()) + (pk,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Record updated"}), 200

# DELETE: Remove a record from a given table.
@app.route('/<table>/<pk>', methods=['DELETE'])
def delete_record(table, pk):
    meta = get_table_metadata(table)
    if not meta or not meta.get("primary_key"):
        return jsonify({"error": "Invalid table or composite primary key not supported"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Check if the record exists
    sql_check = f"SELECT 1 FROM {table.upper()} WHERE {meta['primary_key']} = %s"
    cursor.execute(sql_check, (pk,))
    exists = cursor.fetchone()
    
    if not exists:
        cursor.close()
        conn.close()
        return jsonify({"message": "Record not found, nothing to delete"}), 404

    # If exists, proceed to delete
    sql_delete = f"DELETE FROM {table.upper()} WHERE {meta['primary_key']} = %s"
    cursor.execute(sql_delete, (pk,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Record deleted"}), 200


# @app.route('/')
# def login_page():
#     return render_template('login.html')

# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')

def create_user_if_needed(username, password, email, cursor):
    cursor.execute(
        "SELECT user_id FROM USER WHERE username = %s OR email = %s",
        (username, email)
    )
    row = cursor.fetchone()

    if row:
        return "", row["user_id"]

    new_user_id = str(uuid.uuid4())
    user_insert_sql = (
        f"INSERT INTO USER (user_id, username, password, email) "
        f"VALUES ('{new_user_id}', '{username}', '{password}', '{email}')"
    )

    return user_insert_sql, new_user_id

@app.route('/register/seller', methods=['POST'])
def seller_register():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    store_name = data.get('store_name')
    business_license = data.get('business_license')
    if not username or not password or not email:
        return jsonify({"error": "Missing username, password, or email"}), 400
    if not store_name or not business_license:
        return jsonify({"error": "Missing store_name or business_license"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT s.user_id
            FROM USER u
            JOIN SELLER s ON u.user_id = s.user_id
            WHERE u.username = %s
        """, (username,))
        seller_row = cursor.fetchone()
        if seller_row:
            return jsonify({"error": "User is already a seller"}), 409
        user_sql, user_id = create_user_if_needed(username, password, email, cursor)
        seller_sql = (
            f"INSERT INTO SELLER (user_id, store_name, business_license) "
            f"VALUES ('{user_id}', '{store_name}', '{business_license}')"
        )
        if user_sql != "":
            cursor.execute(user_sql)
        cursor.execute(seller_sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Database error: {e}"}), 400
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message": "Seller registration successful", "user": username}), 201

@app.route('/register/admin', methods=['POST'])
def admin_register():
    data = request.get_json(silent=True)
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    admin_level = data.get('admin_level', '1')
    if not username or not password or not email:
        return jsonify({"error": "Missing username, password, or email"}), 400
    if not admin_level:
        return jsonify({"error": "admin_level is required for admin"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT a.user_id
            FROM USER u
            JOIN ADMIN a ON u.user_id = a.user_id
            WHERE u.username = %s
        """, (username,))
        admin_row = cursor.fetchone()
        if admin_row:
            return jsonify({"error": "User is already an admin"}), 409
        user_sql, user_id = create_user_if_needed(username, password, email, cursor)
        admin_sql = (
            f"INSERT INTO ADMIN (user_id, admin_level) "
            f"VALUES ('{user_id}', '{admin_level}')"
        )
        if user_sql != "":
            cursor.execute(user_sql)
        cursor.execute(admin_sql)
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({"error": f"Database error: {err}"}), 400
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message": "Admin registration successful", "user": username}), 201

@app.route('/register/customer', methods=['POST'])
def customer_register():
    data = request.get_json(silent=True)
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')
    phone = data.get('phone', '')
    if not username or not password or not email:
        return jsonify({"error": "Missing username, password, or email"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT c.user_id
            FROM USER u
            JOIN CUSTOMER c ON u.user_id = c.user_id
            WHERE u.username = %s
        """, (username,))
        customer_row = cursor.fetchone()
        if customer_row:
            return jsonify({"error": "User is already a customer"}), 409
        user_sql, user_id = create_user_if_needed(username, password, email, cursor)
        customer_sql = (
            f"INSERT INTO CUSTOMER (user_id, first_name, last_name, phone) "
            f"VALUES ('{user_id}', '{first_name}', '{last_name}', '{phone}')"
        )
        if user_sql != "":
            cursor.execute(user_sql)
        cursor.execute(customer_sql)
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({"error": f"Database error: {err}"}), 400
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message": "Customer registration successful", "user": username}), 201

@app.route('/login/seller', methods=['POST'])
def seller_login():
    data = request.get_json(silent=True)
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_id FROM USER WHERE username = %s AND password = %s", (username, password))
        user_row = cursor.fetchone()
        if not user_row:
            return jsonify({"error": "Invalid credentials"}), 401
        cursor.execute("""
            SELECT s.user_id
            FROM SELLER s
            WHERE s.user_id = %s
        """, (user_row["user_id"],))
        seller_row = cursor.fetchone()
        if not seller_row:
            return jsonify({"error": "User is not a seller"}), 403
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message": "Seller login successful", "user": username}), 200

@app.route('/login/admin', methods=['POST'])
def admin_login():
    data = request.get_json(silent=True)
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_id FROM USER WHERE username = %s AND password = %s", (username, password))
        user_row = cursor.fetchone()
        if not user_row:
            return jsonify({"error": "Invalid credentials"}), 401
        cursor.execute("""
            SELECT a.user_id
            FROM ADMIN a
            WHERE a.user_id = %s
        """, (user_row["user_id"],))
        admin_row = cursor.fetchone()
        if not admin_row:
            return jsonify({"error": "User is not an admin"}), 403
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message": "Admin login successful", "user": username}), 200

@app.route('/login/customer', methods=['POST'])
def customer_login():
    data = request.get_json(silent=True)
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_id FROM USER WHERE username = %s AND password = %s", (username, password))
        user_row = cursor.fetchone()
        if not user_row:
            return jsonify({"error": "Invalid credentials"}), 401
        cursor.execute("""
            SELECT c.user_id
            FROM CUSTOMER c
            WHERE c.user_id = %s
        """, (user_row["user_id"],))
        customer_row = cursor.fetchone()
        if not customer_row:
            return jsonify({"error": "User is not a customer"}), 403
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message": "Customer login successful", "user": username}), 200


# # 10. Login route
# @app.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')

#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     query = "SELECT * FROM USER WHERE username = %s AND password = %s"
#     cursor.execute(query, (username, password))
#     user = cursor.fetchone()
#     cursor.close()
#     conn.close()

#     if user:
#         return jsonify({"message": "Login successful", "user": user['username']})
#     else:
#         return jsonify({"error": "Invalid credentials"}), 401

# @app.route('/register', methods=['POST'])
# def register():
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')
#     email = data.get('email')

#     if not username or not password or not email:
#         return jsonify({"error": "Missing fields"}), 400

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # Check if username or email already exists
#     cursor.execute("SELECT * FROM USER WHERE username = %s OR email = %s", (username, email))
#     if cursor.fetchone():
#         cursor.close()
#         conn.close()
#         return jsonify({"error": "Username or email already exists"}), 409

#     user_id = str(uuid.uuid4())  # Generate unique user_id
#     query = "INSERT INTO USER (user_id, username, password, email) VALUES (%s, %s, %s, %s)"
#     cursor.execute(query, (user_id, username, password, email))
#     conn.commit()

#     cursor.close()
#     conn.close()

#     return jsonify({"message": "Registration successful", "user": username})



# 11.logout route
@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Logged out"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
