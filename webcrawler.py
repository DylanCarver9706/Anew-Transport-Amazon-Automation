import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

driver=webdriver.Chrome()

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
    try:
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, '#txt_search_ajax_loader[style*="display: none;"]'))
        )
        print("Loading spinner has disappeared.")
    except TimeoutException:
        print("Loading spinner did not disappear within the specified time.")

def log_in(login_url, username, password):
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

# Not currently working
# def logout(driver):
#     # Click on the user dropdown menu
#     user_dropdown = wait_for_element(By.CLASS_NAME, 'dropdown-toggle')
#     user_dropdown.click()

#     # Click on the logout link
#     logout_link = wait_for_element(By.XPATH, '//a[contains(@href, "abd_logout.php")]')
#     logout_link.click()
#     time.sleep(2)
    
def update_order(order_number, dashboard_url):

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
    search_results = wait_for_element(By.ID, 'search_results')

    time.sleep(2)
    
    # Check if there are any search results
    if "There are no results for this search." in search_results.text:
        print("Error: No results found for this search.")
        driver.get(dashboard_url)
        wait_for_url(dashboard_url)
        return "Error: No results found for this search."
    
    # Find the first anchor tag within search results
    # first_result = wait_for_element(By.TAG_NAME, 'a')
    first_result = search_results.find_element(By.TAG_NAME, 'a')
    
    # Extract the href attribute
    href = first_result.get_attribute("href")
    
    # Navigate to the link
    driver.get(href)

    # Wait for the select element with id=status_child to appear
    ##########################################################################
    # This is the code to select the "Invoice Sent" option
    ##########################################################################
    # status_select = wait_for_element(By.ID, 'status_child')
    
    # Select the option "Invoice Sent"
    # select = Select(status_select)
    # select.select_by_visible_text("Invoice Sent")
    ##########################################################################
    driver.get(dashboard_url)
    wait_for_url(dashboard_url)
    return "Success"

def update_order_child_statuses(
        order_number_list, 
        username, 
        password,
        login_url="https://secure.proabd.com/abd_login.php", 
        dashboard_url="https://secure.proabd.com/dashboard.php"
    ):

    orders = []

    try:
        log_in(login_url, username, password)
        
        # Wait until the URL changes to the desired URL
        if not wait_for_url(dashboard_url, timeout=1000):
            print("Timeout: Page did not load within the specified time.")
            driver.quit()
            return
        
        for order_number in order_number_list:
            order = {
                "order_number": order_number,
                "status": update_order(order_number, dashboard_url)
            }
            orders.append(order)
            print(f"Order {order_number} iterated.")

        # logout(driver)

    except Exception as e:
        print("Error: An error occurred while updating the order: {}".format(e))
        # wait_for_user_input()
        return
    
    # Close the browser
    # wait_for_user_input()
    # driver.quit()
    return orders

# Example usage
# order_number_list = ["FSF - 29786209", "FSF - 2978620900", "FSF - 29786209"]
# order_number_list = ["FSF - 29786209"]
# username = ""
# password = ""
# orders = update_order_child_statuses(order_number_list, username, password)
# print(orders)
