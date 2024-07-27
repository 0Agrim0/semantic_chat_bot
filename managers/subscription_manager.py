import requests
from state_managment import set_state
from managers.consumer_manager import Consumer_Manager

cm = Consumer_Manager()


class Subscription_Manager:

    def __init__(self, phone):
        self.phone = phone

    def subscription_check(self, phone):
        consumer_id = cm.get_consumer_id(phone)
        data = requests.get(
            "https://api.crofarm.com/bot/consumer/subscription/v1/?consumer_id={}".format(consumer_id)).json()
        print(data)
        is_active = data.get('having_subscription_items')
        print(is_active)
        if is_active:
            set_state(phone, 'consumer_question_manager', 'subscription_question')
            return "Please select the issue you are facing regarding Subscription:- \n\n 1.Unable to add item Subsciption\n\n 2.Order not placed Subsciption\n\n 3.Manage and Pause Subscription \n\n 4.Any Other Issue \n\n 5.Go Back"
        else:
            return "You do not have any active subscription. \n\n Please click on the below link to know more about subscription and subscribe items:- \n\n https://app.otipy.com/MySubscription \n\n If you need more help, I can connect with the agent."
        # print(data.json())

    def unable_to_add_item_subscription(self):
        msg = '''You can add/pause/remove items in subscription though "My Subscription" page on app. Please click on the below link to open "My Subscription" page:- \n 
                https://app.otipy.com/MySubscription \n If you need more help, I can connect with agent.'''
        return msg

    def order_not_placed_subscription(self):
        consumer_id = cm.get_consumer_id(self.phone)
        api = "https://api.crofarm.com/bot/consumer/subscription/v1/?consumer_id={}".format(consumer_id)
        data = requests.get(api).json()
        print(data)
        c = 1
        order_items = ""
        for item in data.get('items'):
            order_items = order_items + str(c) + ". " + item['name'] + "\n\n"
            c=c+1
        order_items=order_items+ str(c)+". Go Back"
        msg = "Please select the item you need help with:- \n\n"+order_items
        set_state(self.phone, 'consumer_question_manager', 'order_not_placed_subscription_question')
        return msg

    def manage_and_pause_subscription(self):
        msg = '''You can add/pause/remove items in subscription though "My Subscription" page on app. Please click on the below link to open "My Subscription" page:- \n 
                        https://app.otipy.com/MySubscription \n If you need more help, I can connect with agent.'''
        return msg

    def function_calling(self, name: str):
        try:
            do = f"{name}"
            if hasattr(self, do) and callable(func := getattr(self, do)):
                ans = func()
                return ans

        except:
            return "Sorry i cant help in this moment .Please try another question or contact with the admin"


if __name__ == "__main__":
    Subscription_Manager().subscription_check(37)
