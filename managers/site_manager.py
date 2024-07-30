import time

from state_managment import set_state
from managers.consumer_manager import Consumer_Manager
import requests
import streamlit as st
import webbrowser
from tools.chitchat_tool import rag_query
from selenium import webdriver
# Importing keys in the program from webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By

class Site_manager:

    def __init__(self, phone):
        self.phone = phone

    # def redirect(self,_url):
    #     link =''
    #     return st.markdown(link, unsafe_allow_html=True)

    def order_site(self):
        # Providing the path of chrome Web driver
        driver = webdriver.Chrome()

        # Open the desired URL
        driver.get("https://www.otipy.com/")
        print("Opened the Otipy website")
        # driver.get("https://www.otipy.com/")
        st.write("1. Open the Otipy Website:"
                 "   Start by launching your preferred web browser and navigating to the Otipy website.")

        time.sleep(5)
        st.write('''2. Close Any Advertisements:
                      Once the website loads, you may encounter advertisements. Look for a close button (usually marked with an “X”) and click on it to dismiss the ads.''')
        driver.find_element(By.CLASS_NAME,"style_icon__nNhfo").click()

        time.sleep(5)
        st.write('''3. Disable Location Services (if prompted):
                        If the website asks for your location, you may choose to disable this feature for privacy reasons. Look for a prompt or pop-up and select the option to decline or turn off location services.''')
        driver.find_element(By.CLASS_NAME,"style_icon__nNhfo").click()

        time.sleep(5)
        st.write('''4. Add the Desired Product to Your Cart:
                          Browse through the product listings and find the item you wish to purchase. Click on the product to view its details. Once you’ve made your selection, click on the “Add to Cart” button to include the product in your shopping cart.''')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        st.write('''5. View Your Cart:
                        After adding the product to your cart, locate and click on the cart icon, usually found at the top right corner of the website. This will take you to the cart page where you can review the items you’ve added.''')
        driver.find_element(By.CLASS_NAME,"style_btn___3zqs").click()
        time.sleep(5)
        driver.find_element(By.CLASS_NAME,"style_cart_icon__i_LCB").click()



        return '''
                    6. Proceed to Checkout
                    Click on the "Checkout" or equivalent button to begin the payment process.
                    7. Enter Shipping Information
                    Provide your delivery address where you want the items to be shipped.
                    Confirm any delivery preferences or instructions if applicable.
                    8. Choose a Payment Method
                    Select your preferred payment method (e.g., credit/debit card, digital wallets, etc.).
                    Enter your payment details as required.
                    9. Review and Confirm Your Order
                    Double-check all the information, including items, shipping address, and payment details.
                    Confirm your order by clicking on the “Place Order” or equivalent button.
                    10. Receive Order Confirmation
                    You should receive an order confirmation via email or in-app notification.
                    This will include details about your order and an estimated delivery time.
                    11. Track Your Order (Optional)
                    If Otipy provides order tracking, use the tracking feature to monitor the status of your delivery.'''



    def function_calling(self, name: str):
        try:
            do = f"{name}"
            print(do)
            if hasattr(self, do) and callable(func := getattr(self, do)):
                ans = func()
                return ans
        except:
            return "Sorry i cant help in this moment .Please try another question or contact with the admin"
