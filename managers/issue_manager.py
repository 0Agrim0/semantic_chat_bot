from state_managment import set_state
from managers.consumer_manager import Consumer_Manager
from managers.payment_manager import Payment_Manager
from managers.subscription_manager import Subscription_Manager
from managers.reward_wallet_manager import Reward_Wallet_Manager
from managers.coupon_offers import Coupon_Offers
from managers.partner_related import Partner_related
from managers.referral_manager import Referral_Manager

CM = Consumer_Manager()
PM = Payment_Manager()

rwm = Reward_Wallet_Manager()
pr = Partner_related()
rm = Referral_Manager()


class Issue_Manager:

    def __init__(self, phone):
        self.phone = phone
        self.consumer_id = CM.get_consumer_id(phone)

    def coupon(self):
        msg = Coupon_Offers(self.phone).coupon_check()
        return msg

    def payment(self):
        print("53874192")
        ans = PM.payment_check(self.consumer_id)
        print(ans)

        return ans

    def freshdaily(self):
        return "FreshDaily flow"

    def referral(self):
        msg = rm.referrl_check(self.consumer_id)
        return msg

    def subscription(self):
        SM = Subscription_Manager(self.phone)
        ans = SM.subscription_check(self.phone)
        return ans

    def refund(self):
        return "refund flow"

    def reward(self):
        msg = rwm.reward_check(self.phone)
        return msg

    def partner(self):
        msg = Partner_related().partner_static(self.phone)
        return msg

    def any_other_issue(self):
        msg = "Please select the issue you need help with :- \n\n 1. Update Profile \n\n 2. Non Serviceable Area \n\n 3. Sedexo Wallet Usage \n\n 4. Refund Into My Account \n\n 5. Go Back"
        set_state(self.phone, 'consumer_question_manager', 'any_another_question')
        return msg

    def function_calling(self, name: str):
        try:
            do = f"{name}"
            if hasattr(self, do) and callable(func := getattr(self, do)):
                ans = func()
                return ans

        except:
            return "Sorry i cant help in this moment .Please try another question or contact with the admin"
