import requests


class Payment_Manager:

    def payment_check(self, consumer_id):
        try:
            data = requests.get(
                'https://api.crofarm.com/bot/consumer/payment/info/v1/?consumer_id={}&last_payment=true'.format(
                    consumer_id)).json()
            transaction_found = data.get('transaction_found', False)
            payment_details = data.get('payment_details', '{}')
            order_found = data.get('order_found', False)
            success = data.get('success', False)
            print(data)
            if transaction_found and order_found and success:
                return (
                    "Your last payment of Rs.{} (done at {}) was successful. Order was placed against this payment, with order id {}.".format(
                        payment_details['amount'], payment_details['created_at'], payment_details['order_id']))

            if transaction_found and order_found == False and success:
                return (
                    "Your last payment of Rs.{} (done at {}) was successful. Order was not placed against this payment.".format(
                        payment_details['amount'], payment_details['created_at']))

            else:
                return "we were not able to find any payment initiated by you in the last 7 days "
        except:
            return "we were not able to find any payment initiated by you in the last 7 days "


if __name__ == "__main__":
    a = Payment_Manager().payment_check(2165300)
    print(a)
