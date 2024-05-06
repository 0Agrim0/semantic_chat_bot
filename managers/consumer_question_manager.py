import re
from managers.consumer_manager import Consumer_Manager
from tools import order_tool
from state_managment import set_state

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
                result = order_tool.prev_state_answer(phone, responses,"Please provide information regarding this order_id = " + str(question), consumer_name)
                # set_state(phone, 'default', 'default')
                return result
        else:
            set_state(phone, 'default', 'default')
            raise "error"
    except:
        set_state(phone, 'default', 'default')
        raise "error"

# if __name__ == '__main__':
#     consumer_name, responses = question_get_order_details(7986640195, "37298452 abcd")
