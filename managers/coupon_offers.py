from state_managment import set_state
from managers.consumer_manager import Consumer_Manager
import requests

cm = Consumer_Manager()


class Coupon_Offers:

    def __init__(self, phone):
        self.phone = phone

    def coupon_check(self):
        msg = '''Select the issue you are facing: \n\n 1.Wallet Recharge \n\n 2.Order Coupon \n\n 3.Go Back'''
        set_state(self.phone, 'consumer_question_manager', 'coupon_question')
        return msg

    def wallet_recharge(self):
        consumer_id = cm.get_consumer_id(self.phone)
        api = "https://api.crofarm.com/bot/consumer/payment/info/v1/?consumer_id={}&days=10".format(consumer_id)
        print(api)
        data = requests.get(api).json()
        print(data)
        transaction_found = data.get('transaction_found')
        wallet_data = data.get('data')
        success = data.get('success')

        msg = "Please select the transaction on which you to apply the offer :- \n\n"
        c = 1
        if transaction_found:
            for i in wallet_data:
                msg = msg + str(c) + ". Rs." + str(i['amount']) + " on " + str(i['created_at']) + " \n\n"
                c = c + 1
            msg = msg + str(c) + ". Go Back"
            set_state(self.phone, "consumer_question_manager", "wallet_coupon_question")

        else:
            msg = "We were not able to find any successful transaction initiated by you in the last 10 days."
        return msg

        # data.

    def order_coupon(self):
        consumer_id = cm.get_consumer_id(self.phone)
        api = "https://api.crofarm.com/bot/consumer/orders/v1/?consumer_id={}".format(consumer_id)
        data = requests.get(api).json()
        print(data)
        having_active_orders = data.get('having_active_orders')
        msg = "Select the order for which you need help:- \n\n"
        c = 1
        if having_active_orders:
            for order in data.get('orders'):
                msg = msg + str(c) + ". " + str(order['order_id']) + "\n\n"
                c = c + 1
            msg = msg + str(c)+". Go Back"
            set_state(self.phone, "consumer_question_manager", "order_coupon_question")
            return msg

        else:
            return "You do not have any orders in the last 3 days. \n\n If you need more help , i can connect with the agent."
        # return data

    def yes(self):
        return "yes"

    def i_already_have_a_coupon(self):
        return "call"

    def function_calling(self, name: str):
        try:
            do = f"{name}"
            print(do)
            if hasattr(self, do) and callable(func := getattr(self, do)):

                ans = func()
                return ans
        except:
            return "Sorry i cant help in this moment .Please try another question or contact with the admin"

#
# if __name__ == "__main__":
#     Coupon_Offers().wallet_recharge(9041646083)
