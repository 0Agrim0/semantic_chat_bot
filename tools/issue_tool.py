from managers import issue_manager
from state_managment import set_state
from semantic_route.issue_route import Semantic_layer_issue_manager
# from managers.question_manager import issue_question
from managers.issue_manager import Issue_Manager


def issue_static_router(phone, query):
    issue_dict = {
        "1": "Coupons and Offers Related",
        "2": "Payments Related",
        "3": "FreshDaily Membership",
        "4": "Referral Related",
        "5": "Subscription Related",
        "6": "Refund into Bank/Card",
        "7": "Reward Wallet Related",
        "8": "Partner Related",
        "9": "Any Other Issue"
    }
    issue_answer = ''' What kind off issue you face \n'''
    for i in issue_dict:
        issue_answer = issue_answer + str(i) + ". " + issue_dict[i] + "\n"
    set_state(phone=phone, main_flow="issue_tool", next_function_call="issue_question")
    return issue_answer


def issue_rag_query(phone, question):
    print("612789301-----------------", question)
    try:
        function = Semantic_layer_issue_manager(question).semantic_query_function()
        print(function)
        if function is None:
            return issue_static_router(phone, query=question)
        else:
            result = Issue_Manager().function_calling(function)
            set_state(phone, main_flow="default", next_function_call="default")
            return result
    except:
        "raise"


if __name__ == "__main__":
    a = issue_static_router("aj")
    print(a)
