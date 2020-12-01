# #!/usr/bin/env python
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import NoSuchElementException        

#Logging Config
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    #datefmt="%m/%d/%Y %I:%M:%S %p",
    #filemode='w',
    filename='selenium-test.log')


# Start the browser and login with standard_user
def login (user, password):
    print ('Starting the browser...')
    # --uncomment when running in Azure DevOps.
    options = ChromeOptions()
    options.add_argument("--headless") 
    driver = webdriver.Chrome(options=options)
    baseUrl = "https://www.saucedemo.com"
    #driver = webdriver.Chrome()
    print ('Browser started successfully. Navigating to the demo page to login.')
    logging.info('Browser started successfully. Navigating to the demo page to login.')
    driver.get(baseUrl)
    driver.find_element_by_css_selector("input[id='user-name']").send_keys(user)
    driver.find_element_by_css_selector("input[id='password']").send_keys(password)
    driver.find_element_by_css_selector("input[id='login-button']").click()
    print(driver.current_url)
    print(baseUrl + "/inventory.html")
    logging.info(baseUrl + "/inventory.html")
    #assert baseUrl + "/inventory.html" == driver.current_url
    if baseUrl + "/inventory.html" == driver.current_url:
        print("### TEST PASSED - " + user + " Logged in Successfully")
        logging.info("### TEST PASSED - " + user + " Logged in Successfully")
    else:
        print("### TEST FAILED - " + user + " unable to login")
        logging.warning("### TEST FAILED - " + user + " unable to login")

    #Add all items to cart
    logging.info("### Start adding items to cart...###")
    items = driver.find_elements_by_css_selector("div.inventory_item")
    successful_btn_index = []
    for item in items:
        btn = item.find_element_by_css_selector("button.btn_primary.btn_inventory")
        item_name = item.find_element_by_css_selector("div.inventory_item_name")
        cart_value_before = 0 if not is_selector_exist("span.shopping_cart_badge", driver) else driver.find_element_by_css_selector("span.shopping_cart_badge").text
        btn.click()
        cart_value_after = driver.find_element_by_css_selector("span.shopping_cart_badge").text
        item_index = items.index(item)
        if int(cart_value_after) == int(cart_value_before) + 1:
            print(item_name.text + " has been added to cart")
            logging.info(item_name.text + " has been added to cart")
            successful_btn_index.append(item_index)
        else:
            print("Failed to add " + item_name.text + " to cart")
            logging.warning("Failed to add " + item_name.text + " to cart")
        time.sleep(1)

    #Check if cart contains all added items
    logging.info("### Checking if items were added to cart... ###")
    cart_value = 0 if not is_selector_exist("span.shopping_cart_badge", driver) else driver.find_element_by_css_selector("span.shopping_cart_badge").text
    print("### Total number of items on Page is: " + str(len(items)))
    logging.info("### Total number of items on Page is: " + str(len(items)))
    print("### Total items in the cart is " + str(cart_value))
    logging.info("### Total items in the cart is " + str(cart_value))
    if str(cart_value) == str(len(items)):
        print("### TEST PASSED - Cart contains all added items for user: " + user)
        logging.info("### TEST PASSED - Cart contains all added items for user: " + user)
    else:
        print("### TEST FAILED- Cart does not contain all added items for user: " + user)
        logging.warning("### TEST FAILED- Cart does not contain all added items for user: " + user)

    #Remove all items from cart
    logging.info("### Start removing items from cart... ###")

    for index in successful_btn_index:
        btn = items[index].find_element_by_css_selector("button.btn_secondary.btn_inventory")
        item_name = items[index].find_element_by_css_selector("div.inventory_item_name")
        old_cart_value = int(driver.find_element_by_css_selector("span.shopping_cart_badge").text)
        btn.click()
        if len(driver.find_elements_by_css_selector("span.shopping_cart_badge")) != 0:
            new_cart_value = int(driver.find_element_by_css_selector("span.shopping_cart_badge").text)
            if new_cart_value == old_cart_value - 1:
                print(item_name.text + " has been successfully removed from cart")
                logging.info(item_name.text + " has been successfully removed from cart")
            else:
                print("Failed to remove " + item_name.text + " from cart")
                logging.warning("Failed to remove " + item_name.text + " from cart")
        else:
            print(item_name.text + " has been removed from cart")
            logging.info(item_name.text + " has been removed from cart")
            print("No more item in the cart")
            logging.info("No more item in the cart")
    
        time.sleep(1)

    #Confirm cart is empty
    logging.info("### Confirming cart is empty... ###")
    if not is_selector_exist("span.shopping_cart_badge", driver):
        print("### TEST PASSED- All items successfully removed from cart for user: " + user)
        logging.info("### TEST PASSED- All items successfully removed from cart for user: " + user)
    else:
        print("### TEST FAILED- Unable to remove some items from the cart for user: " + user)
        logging.warning("### TEST FAILED- Unable to remove some items from the cart for user: " + user)

def is_selector_exist(selector, driver = None, webelement = None):
    if driver != None:
        counter_element = driver.find_elements_by_css_selector(selector)
    else:
        if webelement != None:
            counter_element = webelement.find_elements_by_css_selector(selector)
        else:
            counter_element = driver.find_elements_by_css_selector(selector)
    if len(counter_element) == 0:
        return False
    else:
        return True

login('standard_user', 'secret_sauce')
login('locked_out_user', 'secret_sauce')
login('problem_user', 'secret_sauce')
login('performance_glitch_user', 'secret_sauce')

