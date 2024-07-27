from state_managment import set_state


class Reward_Wallet_Manager:

    def reward_check(self, phone):

        set_state(phone, 'consumer_question_manager', 'reward_question')
        msg = '''Select the issue you are facing regarding reward wallet. \n\n 1.How to use.\n\n 2.Reward Bonus not received \n\n 3.Bonus Expired \n\n 4.Reward Wallet Summary \n\n5.Go Back'''
        return msg


    def how_to_use(self):
        msg = "Reward Wallet can be used on fruits & vegetables and staples like Atta,Oil,Ghee etc excluding Patato,Onion,Tomato,Coconut and monthly subscription. Applicable amount will be auto applied on the cart."
        return msg

    def reward_bonus_not_received(self):
        return "pass"

    def bonus_expired(self):
        return "pass"

    def reward_wallet_summary(self):
        msg = "You can check the reward wallet summary by clicking on the bellow link:- \n http://app.otipy.com/RewardWallet \n If you need more help ,I can join you with agent"
        return msg

    def function_calling(self, name: str):
        try:
            do = f"{name}"
            if hasattr(self, do) and callable(func := getattr(self, do)):
                ans = func()
                return ans

        except:
            return "Sorry i cant help in this moment .Please try another question or contact with the admin"
