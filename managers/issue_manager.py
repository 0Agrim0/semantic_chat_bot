from state_managment import set_state

class Issue_Manager:

    def coupon(self):
        return "coupon flow"

    def payment(self):
        return "payment flow"

    def freshdaily(self):
        return "FreshDaily flow"

    def referral(self):
        return "referral flow"

    def subscription(self):
        return "subscription flow"

    def refund(self):
        return "refund flow"

    def reward(self):
        return "reward flow"

    def partner(self):
        return "partner flow"

    def any_other_issue(self):
        return "any_other_issue"

    def function_calling(self, name: str):
        try:
            do = f"{name}"
            if hasattr(self, do) and callable(func := getattr(self, do)):
                ans = func()
                return ans

        except:
            return "Sorry i cant help in this moment .Please try another question or contact with the admin"
