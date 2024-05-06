from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI
from semantic_route.order_route import Semantic_layer_order_manager
from managers.consumer_manager import Consumer_Manager
import os
from state_managment import get_state, set_state
from dotenv import load_dotenv

load_dotenv()
CM = Consumer_Manager()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv('GOOGLE_AI_CREDENTIALS')

llm = ChatVertexAI(model="gemini-pro")

template = """
   You are the Otipy chatbot which help the consumer to answer the question of consumer
   Which related to consumer order,
   And in order details you only get when order is delivered and which items are in that order ,
   and total cost of the order, status of order Delivered,Pending,Cancel and Return.
   or if consumer asked about old order then provide last some order ids to the consumer 
   then he select the order id to get the details of order.
   
   Please give ans according to the directly or if context is empty say 'Sorry i don't know'
   


   Consumer_name: {consumer_name}
   Question: {question}

   Answer:  {context}
    
    Important :

        Do not make the answer.
        
   """
custom_rag_prompt = ChatPromptTemplate.from_template(template)

chain = (
        {
            "context": itemgetter("context"),
            "consumer_name": itemgetter("consumer_name"),
            "question": itemgetter("question"),
        }
        | custom_rag_prompt
        | llm
        | StrOutputParser()
)


def route_query(phone, query):
    function_name = Semantic_layer_order_manager(question=query).semantic_query_function()
    print(function_name)
    if function_name is None:
        function_name = "out_context"
    consumer_name = CM.get_consumer_name(phone=phone)
    CM.set_consumer_question(query)
    context = CM.function_calling(function_name)

    return context, consumer_name


def prev_state_answer(phone, context, query, consumer_name):
    result = order_rag_query(phone, query, context, consumer_name)
    return result


def order_rag_query(phone, query, context='', consumer_name=''):
    if context == '' and consumer_name == '':
        context, consumer_name = route_query(phone=phone, query=query)
    print(context)
    print(consumer_name, query)
    # result = chain.invoke({"context": context, "consumer_name": consumer_name, "question": query})

    return context

# if __name__ == "__main__":
#     a = order_rag_query(7986640195, "where is my last order?")
#     print(a)
