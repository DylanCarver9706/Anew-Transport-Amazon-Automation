import json
import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)

# Open the JSON file
with open('auth.json', 'r') as file:
    # Load the JSON data
    auth_data = json.load(file)

# Connect to the MySQL database
conn = mysql.connector.connect(
    host=auth_data["database_host"],
    user=auth_data["database_user"],
    password=auth_data["database_password"],
    database=auth_data["database_database"]
)

@app.route('/orders', methods=['POST'])
def create_order():
# def create_order(data):
    data = request.json
    status = data['status']
    order_number = data['order_number']

    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (status, order_number) VALUES (%s, %s)", (status, order_number))
    conn.commit()
    cursor.close()

    return jsonify({"message": "Order created successfully"}), 201
    # return {"message": "Order created successfully"}

# @app.route('/orders', methods=['GET'])
def get_orders():
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    cursor.close()

    # return jsonify(orders), 200
    return orders

@app.route('/orders/<order_number>', methods=['GET'])
def get_order_by_order_number_api(order_number):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE order_number = %s", (order_number,))
    order = cursor.fetchone()
    cursor.close()

    if order:
        return jsonify(order), 200
    else:
        return jsonify({"message": "Order not found"}), 404

    # if order:
    #     return order
    # else:
    #     return {"message": "Order not found"}

# @app.route('/orders/<order_number>', methods=['GET'])
def get_order_by_order_number(order_number):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE status = %s", (order_number))
    order = cursor.fetchone()
    cursor.close()

    # if order:
    #     return jsonify(order), 200
    # else:
    #     return jsonify({"message": "Order not found"}), 404

    if order:
        return order
    else:
        return {"message": "Order not found"}

@app.route('/orders/created', methods=['GET'])
def get_created_orders():
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE status = 'created'")
    created_orders = cursor.fetchall()
    cursor.close()

    if created_orders:
        return jsonify(created_orders), 200
    else:
        return jsonify({"message": "No orders with status 'created' found"}), 404

def update_order(order_id, new_status):
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = %s WHERE id = %s", (new_status, order_id))
    conn.commit()
    cursor.close()

if __name__ == '__main__':
    app.run(debug=True)

# print(get_order_by_order_number("ABC123"))
# print(create_order({"status": "123", "order_number": "321"}))
# print(get_orders())
# print(update_order(4, "Update Test"))