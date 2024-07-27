from managers import issue_manager
from state_managment import set_state
from semantic_route.issue_route import Semantic_layer_issue_manager
# from managers.question_manager import issue_question
from managers.issue_manager import Issue_Manager
from managers.consumer_manager import Consumer_Manager
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI
from semantic_route.order_route import Semantic_layer_order_manager
from managers.consumer_manager import Consumer_Manager
import os
from state_managment import get_state, set_state
from dotenv import load_dotenv
from lang_guidance import laguage_detector

CM = Consumer_Manager()

llm = ChatVertexAI(model="gemini-pro")

template = """
    Check the answer is related to the question. If yes then answer it.If not then say 'Sorry i cant help you'
    Please change this text in this language {language}.And Please do not add anything in the answer. 

   Consumer_name: {consumer_name}
   Question: {question}

   Answer:  {context}

    Important :
        Just provide the answer.
        Do not give question and consumer name.
        Do not give important note with answer.

   """
custom_rag_prompt = ChatPromptTemplate.from_template(template)

chain = (
        {
            "context": itemgetter("context"),
            "consumer_name": itemgetter("consumer_name"),
            "question": itemgetter("question"),
            "language": itemgetter("language"),
        }
        | custom_rag_prompt
        | llm
        | StrOutputParser()
)


def issue_static_router(phone, query):
    try:
        consumer_name = CM.get_consumer_name(phone)
        print(consumer_name)
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
    except:
        return "Your number is not registered with us. To access our services seamlessly."


def issue_rag_query(phone, question):
    print("612789301-----------------", question)
    try:
        function = Semantic_layer_issue_manager(question).semantic_query_function()
        print(function)
        # consumer_name = CM.get_consumer_name(phone)
        # lang = laguage_detector(question)
        # print(lang)
        if function is None:
            return issue_static_router(phone, query=question)
        elif function is 'default':
            return issue_static_router(phone, query=question)
        else:
            set_state(phone, main_flow="default", next_function_call="default")
            fun_result = Issue_Manager(phone).function_calling(function)

        # if lang['language'] != 'English':
        #     result = chain.invoke(
        #         {"context": fun_result, "consumer_name": consumer_name, "question": question,
        #          "language": lang['language']})
        # else:
        #     result = fun_result
            return fun_result
    except:
        "raise"


if __name__ == "__main__":
    a = issue_static_router("aj")
    print(a)
