from state_managment import set_state


class Partner_related:

    def partner_static(self, phone):
        msg = "Please select the topic for which you need support:- \n\n 1.Partner Refused Delivery \n\n 2.Parten non contactable  \n\n 3.Partner asking commission \n\n 4.Join Otipy as partner \n\n 5.Go Back"
        set_state(phone, 'consumer_question_manager', 'partner_question')
        return msg

    def partner_refused_delivery(self):
        msg = "raise call"
        return msg

    def partner_non_contactable(self):
        msg = "rase call"
        return msg

    def partner_asking_commission(self):
        msg = "raise call"
        return msg

    def join_otipy_as_partner(self):
        msg = "We are glad to know that.\n\n Please click on this link to fill the form and one of our representative would call you in no time: \n\n https://otipy.com/partner "
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
