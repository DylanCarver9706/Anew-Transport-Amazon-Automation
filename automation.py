import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

# Get query headers
with open("pro_request_headers.json", "r") as file:
    # Load the JSON data from the file into a Python dictionary
    query_headers = json.load(file)

def convert_cookie():
    # Open the file in read mode
    with open("cookies.txt", "r") as file:
        # Read the contents of the file into a string variable
        file_contents = file.read()

    webscraper_cookie = []
    request_cookie = {}
    
    for cookie in file_contents.split("; "):
        name, value = cookie.split("=")
        webscraper_cookie.append({'name': name, 'value': value})
        request_cookie[name] = value
    
    return webscraper_cookie, request_cookie

# Get cookies data
webscraper_cookie, request_cookie = convert_cookie()

def wait_for_url(driver, target_url, timeout=1000):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if driver.current_url == target_url:
            return True
        time.sleep(1)  # Adjust sleep time as needed
    return False

def wait_for_element(driver, by, value, timeout=1000):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def query_order(order_number):

    data = 'searchword={}'.format(order_number)

    response = requests.post('https://secure.proabd.com/abd_search.php', cookies=request_cookie, headers=query_headers, data=data)

    soup = BeautifulSoup(response.text, "html.parser")

    # print(response.text)

    if "There are no results for this search" in response.text:
        # driver.quit()
        return "Error: No result found"
    elif soup.find('ul', class_='list-group').find('a'):
        # If there is an <a> tag within the <ul> element
        result_href = soup.find('ul', class_='list-group').find('a')['href']
        return result_href
    else:
        # If there is no <a> tag within the <ul> element
        return "Error: No result found"
    


def update_child_status(order_number):
    # Launch a browser

    driver = webdriver.Chrome()

    try:
        url = query_order(order_number)
        
        if url == "Error: No result found":
            driver.quit()
            return {"outcome": "Error: No result found"}

        # Open the URL
        driver.get('https://secure.proabd.com/dashboard.php')

        for cookie in webscraper_cookie:
            driver.add_cookie(cookie)

        driver.get(url)
        wait_for_url(driver, url)

        # time.sleep(5)
        select_element = wait_for_element(driver, By.ID, "status_child")

        # Create a Select object
        select = Select(select_element)

        # Select the option with value "4768"
        select.select_by_visible_text("Invoice Sent")

        return {"outcome": "Updated"}
    except Exception as e:
        print("An error occurred:", e)
        return {"outcome": "Error: {}".format(e)}
    finally:
        # Close the browser
        driver.quit()

@app.route('/update_order', methods=['POST'])
def api():
    # Assuming the request contains JSON data
    request_data = request.get_json()

    print(request_data)

    # Validate the data

    response_data = update_child_status(request_data["order_number"])
    print(response_data)
    # Return a JSON response
    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(debug=True)
