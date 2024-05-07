import re
from managers.consumer_manager import Consumer_Manager
from tools import order_tool,issue_tool
from state_managment import set_state
# from semantic_route.issue_route import Semantic_layer_issue_manager
from managers.issue_manager import Issue_Manager


CM = Consumer_Manager()


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
    print("1897498237984",question)
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
        print("-------------------",func_question)
        # function_call = Semantic_layer_issue_manager.semantic_query_function(func_question)
        result = Issue_Manager().function_calling(func_question)
        # set_state(phone,'default','default')
        return result
    except:
        set_state(phone, 'default', 'default')
        raise




if __name__ == '__main__':
    consumer_name, responses = issue_question(7986640195, "6")
