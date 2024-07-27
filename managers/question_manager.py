import re
from managers.consumer_manager import Consumer_Manager
from tools import order_tool, issue_tool
from state_managment import set_state
# from semantic_route.issue_route import Semantic_layer_issue_manager
from managers.issue_manager import Issue_Manager
from managers.subscription_manager import Subscription_Manager
from managers.reward_wallet_manager import Reward_Wallet_Manager
from managers.coupon_offers import Coupon_Offers
from managers.partner_related import Partner_related
from managers.any_another_issue import Any_another_issue
from tools.issue_tool import issue_static_router
import requests

CM = Consumer_Manager()

rwd = Reward_Wallet_Manager()


def question_get_order_details(phone, question):
    try:
        question = question.split(" ")
        order_id = []
        for ques in question:
            res = re.sub("\D", "", ques)
            if res:
                order_id.append(res)
        if len(order_id) > 0:
            consumer_name = CM.get_consumer_name(phone=phone)
            responses = ""
            for ids in order_id:
                if len(ids) > 0:
                    f_res = CM.get_order_details(int(ids))
                    print(f_res)
                    if f_res is not None:
                        responses = responses + " \n" + str(f_res)
                    else:
                        pass
            if responses == "":
                return "Please write correct order id from above."
            else:
                result = order_tool.prev_state_answer(phone, responses,
                                                      "Please provide information regarding this order_id = " + str(
                                                          question), consumer_name)
                # set_state(phone, 'default', 'default')
                return result
        else:
            set_state(phone, 'default', 'default')
            raise "error"
    except:
        set_state(phone, 'default', 'default')
        raise "error"


def issue_question(phone, question):
    print("1897498237984", question)
    try:
        issue_dict = {
            "1": "coupon",
            "2": "payment",
            "3": "freshdaily",
            "4": "referral",
            "5": "subscription",
            "6": "refund",
            "7": "reward",
            "8": "partner",
            "9": "any_other_issue"
        }
        func_question = issue_dict[question]
        print("-------------------", func_question)
        # function_call = Semantic_layer_issue_manager.semantic_query_function(func_question)
        result = Issue_Manager(phone).function_calling(func_question)
        # set_state(phone,'default','default')
        return result
    except:
        set_state(phone, 'default', 'default')
        raise


def subscription_question(phone, question):
    try:
        # question = re.sub("\D", "", question)
        # print(question)
        SM = Subscription_Manager(phone)
        sub_dict = {
            "1": "Unable to add item Subscription",
            "2": "Order not placed Subscription",
            "3": "Manage and Pause Subscription",
            "4": "Any Other Issue",
            "5": "Go Back"
        }
        sub_func = sub_dict.get(question)
        function_name = "_".join(sub_func.lower().split(" "))
        if function_name == "go_back":
            return issue_static_router(phone, "")
        ans = SM.function_calling(function_name)
        return ans
    except:
        try:
            function_name = "_".join(question.lower().split(" "))
            ans = SM.function_calling(function_name)
            if ans:
                return ans
            else:
                set_state(phone, 'default', 'default')
                raise
        except:
            set_state(phone, 'default', 'default')
            raise


def order_not_placed_subscription_question(phone, question):
    try:
        consumer_id = CM.get_consumer_id(phone)
        api = "https://api.crofarm.com/bot/consumer/subscription/v1/?consumer_id={}".format(consumer_id)
        data = requests.get(api).json()
        print(data)
        order_dict = {}
        c = 1
        for item in data.get('items'):
            order_dict[str(c)] = item['id']
            c = c + 1
        # print(order_dict[question])

        order_dict[str(c)]="go_back"
        print(order_dict)
        if order_dict.get(question)=="go_back":
            return Subscription_Manager(phone).subscription_check(phone)
        api = "https://api.crofarm.com/bot/consumer/subscription/item/v1/?subscription_item_id={}".format(
            order_dict[str(question)])
        data = requests.get(api).json()
        order_placed = data.get('order_placed')
        is_paused = data.get('is_paused')
        if order_placed:
            return "Your order has been successfully placed. You can check the order details by clicking on the link below:- \n\n http://app.otipy.com/Order"
        if is_paused:
            return '''You can add/pause/remove items in subscription through "My Subscription" page on app.Please click on the below link to open "My Subscription" pages:- \n\n https://app.otipy.com/MySubscription'''
        else:
            return "Your subscription for the selected item is not eligible for today's delivery."
    except:
        set_state(phone, "default", "default")
        raise


def reward_question(phone, question):
    try:
        reward_dict = {
            "1": "How to use",
            "2": "Reward Bonus not received",
            "3": "Bonus Expired",
            "4": "Reward Wallet Summary",
            "5": "Go Back"
        }
        fun = reward_dict.get(question)
        function_name = "_".join(fun.lower().split(" "))
        print(function_name)
        if function_name == "go_back":
            return issue_static_router(phone, "")
        result = rwd.function_calling(function_name)
        return result
    except:
        try:
            function_name = "_".join(question.lower().split(" "))
            ans = rwd.function_calling(function_name)
            if ans:
                return ans
            else:
                set_state(phone, 'default', 'default')
                raise
        except:
            set_state(phone, 'default', 'default')
            raise


def coupon_question(phone, question):
    co = Coupon_Offers(phone)
    try:
        coupon_dict = {"1": "Wallet Recharge", "2": "Order Coupon", "3": "Go Back"}

        fun = coupon_dict.get(question)
        function_name = "_".join(fun.lower().split(" "))
        print(function_name)
        if function_name == "go_back":
            return issue_static_router(phone, question)
        result = co.function_calling(function_name)
        print(result)
        return result
    except:
        try:
            function_name = "_".join(question.lower().split(" "))
            ans = co.function_calling(function_name)
            if ans:
                return ans
            else:
                set_state(phone, 'default', 'default')
                raise
        except:
            set_state(phone, 'default', 'default')
            raise


def partner_question(phone, question):
    try:
        partner_dict = {"1": "Partner Refused Delivery",
                        "2": "Partner non contactable",
                        "3": "Partner asking commission",
                        "4": "Join Otipy as partner",
                        "5": "Go back"}
        fun = partner_dict.get(question)
        function_name = "_".join(fun.lower().split(" "))
        if function_name == "go_back":
            return issue_static_router(phone, "")
        result = Partner_related().function_calling(function_name)
        return result
    except:
        try:
            function_name = "_".join(question.lower().split(" "))
            ans = Partner_related().function_calling(function_name)
            if ans:
                return ans
            else:
                set_state(phone, 'default', 'default')
                raise
        except:
            set_state(phone, 'default', 'default')
            raise


def any_another_question(phone, question):
    try:
        any_another_dict = {
            "1": "Update Profile",
            "2": "Non Serviceable Area",
            "3": "Sedexo Wallet Usage",
            "4": "Refund Into My Account",
            "5": "Go Back"
        }
        fun = any_another_dict.get(question)
        function_name = "_".join(fun.lower().split(" "))
        # print(function_name)
        if function_name == "go_back":
            return issue_static_router(phone, "")
        result = Any_another_issue(phone).function_calling(function_name)
        return result
    except:
        try:
            function_name = "_".join(question.lower().split(" "))
            ans = Any_another_issue(phone).function_calling(function_name)
            if ans:
                return ans
            else:
                set_state(phone, 'default', 'default')
                raise
        except:
            set_state(phone, 'default', 'default')
            raise


def update_profile_question(phone, question):
    try:
        update_dict = {
            "1": "Update address",
            "2": "update Delivery preference",
            "3": "Delete Otipy Account",
            "4": "Go Back"
        }
        fun = update_dict.get(question)
        function_name = "_".join(fun.lower().split(" "))
        # print(function_name)
        if function_name == "go_back":
            return Any_another_issue(phone).function_calling("any_another_issue")
        result = Any_another_issue(phone).function_calling(function_name)
        return result
    except:
        try:
            function_name = "_".join(question.lower().split(" "))
            ans = Any_another_issue(phone).function_calling(function_name)
            if ans:
                return ans
            else:
                set_state(phone, 'default', 'default')
                raise
        except:
            set_state(phone, 'default', 'default')
            raise


def wallet_coupon_question(phone, question):
    try:
        co = Coupon_Offers(phone)
        consumer_id = CM.get_consumer_id(phone)
        api = "https://api.crofarm.com/bot/consumer/payment/info/v1/?consumer_id={}&days=10".format(consumer_id)
        data = requests.get(api).json()
        wallet_dict = {}
        c = 1
        for rs in data.get("data"):
            wallet_dict[str(c)] = rs['id']
            c = c + 1
        wallet_dict[str(c)] = "go_back"
        if wallet_dict.get(question) == "go_back":
            return co.function_calling("coupon_check")
        payment_check = "https://api.crofarm.com/bot/consumer/payment/info/v1/?payment_id={}".format(
            wallet_dict[question])
        payment_data = requests.get(payment_check).json()
        if payment_data.get('coupon_id'):
            return "You have already applied coupon on this transaction and promo amount of {} was deposited in your reward wallet.You can only apply one coupon code on one transaction.".format(
                payment_data.get("coupon_amount"))
        else:
            set_state(phone, "consumer_question_manager", "best_offer_question")
            return "Do you want us to apply the best offer on you transaction? \n\n 1.Yes \n\n 2.I already have a coupon \n\n 3.Go Back"
    except:
        raise


def best_offer_question(phone, question):
    co = Coupon_Offers(phone)
    best_offer_dict = {"1": "Yes",
                       "2": "I already have a coupon",
                       "3": "Go back"}
    fun = best_offer_dict.get(question)
    function_name = "_".join(fun.lower().split(" "))
    print(function_name)
    if function_name == "go_back":
        return co.function_calling("wallet_recharge")
    result = co.function_calling(function_name)
    print(result)
    return result


# def order_coupon_question(phone,question):
#


if __name__ == '__main__':
    consumer_name, responses = issue_question(7986640195, "6")
