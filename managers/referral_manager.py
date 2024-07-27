import requests


class Referral_Manager:

    def referrl_check(self, consumer_id):
        data = requests.get(
            "https://api.crofarm.com/bot/consumer/referral/v2/?consumer_id={}".format(consumer_id)).json()
        referral_cx_found = data.get('referral_cx_found')
        success_referral = data.get('success_referral')
        pending_referral = data.get('pending_referral')
        success = data.get('success')
        print(data)
        if success_referral['found'] == False and pending_referral['found']:
            return "You do not have any referrals where reward is credited. \n\n Please find the list of referee who have signed up but no order has been successfully delivered:- \n\n {}".format(
                data.get('pending_referral')['txt'])
        elif success_referral['found'] == 'True':
            return "Please find the list of successful referrals where reward was credited into your account :- \n\n{}  \n\n Please find the list of referrals where referee has signed up but reward was not credited because no order has been successfully delivered :- {}  \n\n If you need more help,I can connect with agent.".format(
                success_referral['txt'], pending_referral['txt'])
        else:
            return "You do not have any referrals where reward is credited."


if __name__ == "__main__":
    a = Referral_Manager().referrl_check(37)
    print(a)
