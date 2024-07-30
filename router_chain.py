# __import__('pysqlite3')
# import sys
#
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from semantic_question import Semantic_layer_question_manager
from tools.chitchat_tool import rag_query
from managers.consumer_manager import Consumer_Manager
from tools.order_tool import order_rag_query
from state_managment import get_state, set_state, add_state
from managers import question_manager
from tools.issue_tool import issue_rag_query
from managers.agent_connect import Agent_connect
from semantic_route.site_route import Semantic_site_manager
from managers.site_manager import Site_manager

CM = Consumer_Manager()


class function_router:

    def __init__(self, phone):
        self.phone = phone
        self.question = ''

    def chitchat_tool(self):
        result = rag_query(query=self.question, phone=self.phone)
        return result

    def order_tool(self):
        order_result = order_rag_query(phone=self.phone, query=self.question)
        return order_result

    def issue_tool(self):
        issue_result = issue_rag_query(self.phone, self.question)
        return issue_result

    def agent_tool(self):
        a = Agent_connect(self.phone, self.question).agent_chat()
        return a

    def site_tool(self):
        function_name = Semantic_site_manager(self.question).semantic_query_function()
        print(function_name)
        result = Site_manager(self.phone).function_calling(function_name)
        return result

    def router(self, query):
        state = get_state()
        try:
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
                    bar = getattr(question_manager, state[str(self.phone)]['next_function_call'])
                    print(bar)
                    result = bar(self.phone, query)
                    return result
                except:
                    ans = self.router(query=query)
                    return ans
        except:
            add_state(self.phone, 'default', 'default')
            ans = self.router(query=query)
            return ans
