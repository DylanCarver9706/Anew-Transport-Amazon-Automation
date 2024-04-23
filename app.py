import threading
from flask import Flask, request, jsonify
import json
import mysql.connector
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

driver=webdriver.Chrome()

login_url="https://secure.proabd.com/abd_login.php"
dashboard_url="https://secure.proabd.com/dashboard.php"

# Open the JSON file
with open('auth.json', 'r') as file:
    # Load the JSON data
    auth_data = json.load(file)

app = Flask(__name__)

# Connect to the MySQL database
conn = mysql.connector.connect(
    host=auth_data["database_host"],
    user=auth_data["database_user"],
    password=auth_data["database_password"],
    database=auth_data["database_database"]
)

@app.route('/api', methods=['POST'])
def api():
    # Assuming the request contains JSON data
    request_data = request.get_json()

    # Validate the data


    response_data = update_order_child_statuses(request_data["order_numbers_list"])
    print(response_data)
    # Return a JSON response
    return jsonify(response_data)

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

def update_order_in_db(order_id, new_status):
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = %s WHERE id = %s", (new_status, order_id))
    conn.commit()
    cursor.close()

def human_typing_delay():
    time.sleep(float("0." + str(random.randint(0, 3)) + str(random.randint(0, 6)) + str(random.randint(0, 9))))

def wait_for_user_input():
    input("Press Enter to exit...")
    driver.quit()

def type_characters(string, driver_element):
    for character in string:
        driver_element.send_keys(character)
        human_typing_delay()

def wait_for_url(target_url, timeout=1000):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if driver.current_url == target_url:
            return True
        time.sleep(1)  # Adjust sleep time as needed
    return False

def wait_for_element(by, value, timeout=1000):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def wait_for_loading_spinner():
    # try:
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, '#txt_search_ajax_loader[style*="display: none;"]'))
    )
    print("Loading spinner has disappeared.")
    # except TimeoutException:
        # print("Loading spinner did not disappear within the specified time.")

def log_in(username, password):
    # Open the URL in the web browser
    driver.get(login_url)
    # Find the username input element and fill it with the provided username
    username_input = wait_for_element(By.ID, "username")
    type_characters(username, username_input)
    
    time.sleep(1)
    
    # Find the password input element and
    password_input = wait_for_element(By.ID, "password")
    type_characters(password, password_input)

    time.sleep(1)

    # Click the login button
    login_button = driver.find_element(By.ID, "button1id")
    login_button.click()
    # Wait for the page to load

def search(order_number):

    # Wait until the search image element is present
    search_img = wait_for_element(By.ID, 'search_img')
    search_img.click()

    # Find the input element for order_id and enter the order_number
    txt_search = driver.find_element(By.ID, 'txt_search')
    type_characters(order_number, txt_search)

    time.sleep(2)
    
    # Find the button element to submit the search
    txt_search_btn = driver.find_element(By.ID, 'txt_search_btn')
    txt_search_btn.click()

    # time.sleep(5)

    # Wait for search results to appear
    wait_for_loading_spinner()
    time.sleep(3)
    search_results = wait_for_element(By.ID, 'search_results')

    time.sleep(3)

    # Find all anchor tags (a) within the div
    a_tags = search_results.find_elements(By.TAG_NAME, 'a')

    # Check if any anchor tags are found
    if len(a_tags) > 0:
        # Click the first anchor tag
        first_a_tag = a_tags[0]
        first_a_tag.click()
        print("Clicked the first <a> tag.")
        wait_for_url(first_a_tag)
        return "Updated"
    else:
        return "Error: No search results found."
        # print("Error: No search results found.")
    
def update_order_in_pro(order_number, dashboard_url):

    order_id = get_order_by_order_number(order_number)

    result = search(order_number, dashboard_url)

    if "Error" in result:
        update_order_in_db(order_id, result)
    
    # Navigate to the link
    # driver.get(result)

    # Wait for the select element with id=status_child to appear
    ##########################################################################
    # This is the code to select the "Invoice Sent" option
    ##########################################################################
    # status_select = wait_for_element(By.ID, 'status_child')
    
    # Select the option "Invoice Sent"
    # select = Select(status_select)
    # select.select_by_visible_text("Invoice Sent")
    ##########################################################################
    # driver.get(dashboard_url)
    # wait_for_url(dashboard_url)
    update_order_in_db(order_id, result)

def update_order_child_statuses(
        order_number_list, 
        # username, 
        # password,
    ):

    try:
        # current_url = driver.current_url
        # if current_url != dashboard_url:
        #     log_in(login_url, username, password)
        
        # Wait until the URL changes to the desired URL
        if not wait_for_url(dashboard_url, timeout=1000):
            print("Timeout: Page did not load within the specified time.")
            driver.quit()
            return
        
        for order_number in order_number_list:
            update_order_in_pro(order_number)
            print(f"Order {order_number} iterated.")

        # logout(driver)

    except Exception as e:
        print("Error: An error occurred while updating the order: {}".format(e))
        # wait_for_user_input()
        return
    
    # Close the browser
    # wait_for_user_input()
    # driver.quit()

if __name__ == '__main__':
    # Call the login function before starting Flask
    # time.sleep(15)
    log_in(auth_data["pro_username"], auth_data["pro_password"])

    app.run(debug=True)

    # Start Flask in a separate thread
    # threading.Thread(target=app.run, kwargs={'debug': True}).start()

# print(get_order_by_order_number("ABC123"))
# print(create_order({"status": "123", "order_number": "321"}))
# print(get_orders())
# print(update_order(4, "Update Test"))