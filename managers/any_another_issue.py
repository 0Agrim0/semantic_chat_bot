from state_managment import set_state
from managers.consumer_manager import Consumer_Manager
import requests

cm = Consumer_Manager()


class Any_another_issue:

    def __init__(self, phone):
        self.phone = phone

    def any_another_issue(self):
        msg = "Please select the issue you need help with :- \n\n 1. Update Profile \n\n 2. Non Serviceable Area \n\n 3. Sedexo Wallet Usage \n\n 4. Refund Into My Account \n\n 5. Go Back"
        set_state(self.phone, 'consumer_question_manager', 'any_another_question')
        return msg

    def update_address(self):
        msg = "Please go to the app to update your address and a delivery partner will be assigned to you based on availability.\n\n Please follow the following steps:- \n\n   1.Go to the app. \n\n   2.Click on Menus on the top left. \n\n    3.Click on Update Profile/Address \n\n   4.Update the address \n\n 5.Go Back"
        return msg

    def update_delivery_preference(self):
        msg = "Please select the delivery preference that you want for you want for your order:- \n\n1.Do not disturb \n\n2.Ring the door bell"
        return msg

    def delete_otipy_account(self):
        msg = "You can now delete ypu account bu dropping an email to care@crofarm.com and we will contact you within 24 hours. \n\n If you need more help,I can connect with agent"
        return msg

    def update_profile(self):
        msg = "Please select the help you need regarding profile:- \n\n 1. Update Address \n\n 2. Update Delivery Preference \n\n 3. Delete Otipy Account \n\n 4. Go Back"
        set_state(self.phone, 'consumer_question_manager', 'update_profile_question')
        return msg

    def non_serviceable_area(self):
        consumer_id = cm.get_consumer_id(self.phone)
        api = "https://api.crofarm.com/bot/consumer/alternate/partners/v1/?consumer_id={}".format(consumer_id)
        data = requests.get(api).json()
        return data

    def sedexo_wallet_usage(self):
        msg = "Sodexo wallet usage is restricted to carts with edible items only, and it will be applied automatically while checkout. "
        return msg

    def refund_into_my_account(self):
        msg = "check for balance"
        return msg

    def function_calling(self, name: str):
        try:
            do = f"{name}"
            print(do)
            if hasattr(self, do) and callable(func := getattr(self, do)):
                ans = func()
                return ans
        except:
            return "Sorry i cant help in this moment .Please try another question or contact with the admin"
