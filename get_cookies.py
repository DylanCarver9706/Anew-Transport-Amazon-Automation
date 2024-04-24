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

login_url="https://secure.proabd.com/abd_login.php"
dashboard_url="https://secure.proabd.com/dashboard.php"

with open("auth.json", "r") as file:
    auth_data = json.load(file)

def human_typing_delay():
    time.sleep(float("0." + str(random.randint(0, 3)) + str(random.randint(0, 6)) + str(random.randint(0, 9))))

def type_characters(string, driver_element):
    for character in string:
        driver_element.send_keys(character)
        human_typing_delay()

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

def get_cookies_after_log_in(username, password):
    # Open the URL in the web browser
    driver=webdriver.Chrome()
    driver.get(login_url)
    # Find the username input element and fill it with the provided username
    username_input = wait_for_element(driver, By.ID, "username")
    type_characters(username, username_input)
    
    time.sleep(1)
    
    # Find the password input element and
    password_input = wait_for_element(driver, By.ID, "password")
    type_characters(password, password_input)

    time.sleep(1)

    # Click the login button
    login_button = driver.find_element(By.ID, "button1id")
    login_button.click()
    
    # Wait for the page to load
    wait_for_url(driver, dashboard_url)

    cookies = driver.get_cookies()
    print(cookies)

    cookie_strings = []
    for cookie in cookies:
        cookie_string = "; ".join([f"{key}={value}" for key, value in cookie.items()])
        cookie_strings.append(cookie_string)

    # Join all cookie strings with a space
    cookies_one_line = " ".join(cookie_strings)

    # Write cookies to a text file
    with open("cookies_test.txt", "w") as file:
        file.write(cookies_one_line)
        # for cookie in cookies:
        #     file.write(cookie)

    print("Cookies written to cookies.txt")

    # Close the WebDriver
    driver.quit()

if __name__ == "__main__":
    get_cookies_after_log_in(auth_data["pro_username"], auth_data["pro_password"])