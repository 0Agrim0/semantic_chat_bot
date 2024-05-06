from semantic_question import Semantic_layer_question_manager
from tools.chitchat_tool import rag_query
from managers.consumer_manager import Consumer_Manager
from tools.order_tool import order_rag_query
from state_managment import get_state, set_state
from managers import consumer_question_manager

CM = Consumer_Manager()


class function_router:

    def __init__(self, phone):
        self.phone = phone
        self.question = ''

    def chitchat_tool(self):
        result = rag_query(query=self.question, phone=self.phone)
        return result

    def order_tool(self):
        a = order_rag_query(phone=self.phone, query=self.question)
        print(a)
        return a

    def router(self, query):
        state = get_state()
        if state[str(self.phone)]['main_flow'] == 'default':
            function = Semantic_layer_question_manager(question=query).semantic_query_function()
            print(function)
            if function is not None:
                self.question = query
                do = f"{function}"
                if hasattr(self, do) and callable(func := getattr(self, do)):
                    ans = func()
                    return ans
            if function is None:
                self.question = query
                ans = self.chitchat_tool()
                return ans
        else:
            try:
                bar = getattr(consumer_question_manager,
                              "question_" + state[str(self.phone)]['next_function_call'])
                result = bar(self.phone, query)
                return result
            except:
                ans = self.router(query=query)
                return ans


if __name__ == "__main__":
    res = function_router(7986640195).router("14134")
    print(res)
