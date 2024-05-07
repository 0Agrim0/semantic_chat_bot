from typing import Tuple, List, Set, Any
from lib import sql_connector
from lib.TimeManager import TimeManager
from state_managment import get_state, set_state
import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI

load_dotenv()
TM = TimeManager()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv('GOOGLE_AI_CREDENTIALS')

llm = ChatVertexAI(model="gemini-pro")

template = """
   You are the Otipy chatbot which help the consumer to answer the question of consumer
    when ever question about "where is my order "please answer with the  latest order 

    consumer_history: {context}

   Consumer_name: {consumer_name}
   Question: {question}

   Answer:  

    Important :
        Please provide simple answer,
        Do not make the answer.
        Do not send consumer name in answer 

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


class Consumer_Manager:

    def set_consumer_question(self, query):
        self.query = query

    def get_consumer_id(self, phone):

        consumer_id = sql_connector.get_sql_data(
            "select id from consumer.cn_consumer where phone='{}';".format(phone))

        if consumer_id:
            self.consumer_id = consumer_id[0][0]
            return self.consumer_id
        else:
            raise "Consumer not registered with Otipy"

    def get_consumer_name(self, phone):
        self.phone = phone
        consumer_info = sql_connector.get_sql_data(
            "select id,name from consumer.cn_consumer where phone='{}';".format(phone))
        if consumer_info:
            self.consumer_id = consumer_info[0][0]
            self.consumer_name = consumer_info[0][1]
            return self.consumer_name
        else:
            raise "Consumer not registered with Otipy"

    def get_consumer_info(self, phone: int) -> tuple[int, str] | str:
        consumer_info = sql_connector.get_sql_data(
            "select id,name from consumer.cn_consumer where phone='{}';".format(phone))
        if consumer_info:
            consumer_id = consumer_info[0][0]
            name = consumer_info[0][1]
            return consumer_id, name
        else:
            print("Your number is not registered with us.")

    def get_last_five_order(self):
        order_id = sql_connector.get_sql_data(
            '''SELECT  id from consumer.cn_order where consumer_id ={} order by id desc limit 5'''.format(
                self.consumer_id))
        id_dict = {}
        id_str = "\n"
        id_key = 1
        for id in order_id:
            id_dict[id_key] = id[0]
            id_str = id_str + str(id_key) + ". " + str(id[0]) + "\n"
            id_key = id_key + 1
        set_state(self.phone, 'consumer_question_manager', 'question_get_order_details')
        self.last_order_dict = id_dict
        return "Your last five order IDs are {} \n Which order information would you like?".format(id_str)

    def get_order_details(self, id):
        # try:
        order_id = id
        self.get_last_five_order()
        order_id = self.last_order_dict.get(id, order_id)

        order_detail = sql_connector.get_sql_data(
            '''with cn_order_data as (
                    select order_id,prod_name from consumer.cn_order_data where order_id = {}
                ),cn_order as (
                    select id,status,total_amount,n_slot_id from consumer.cn_order where consumer_id={}
                )
                select * from cn_order_data left join cn_order on cn_order_data.order_id=cn_order.id where id is not null
            '''.format(order_id, self.consumer_id))
        print(order_detail)

        if order_detail:
            product_name = ""
            status = ""
            price = ""
            delivery_date = ""

            for detail in order_detail:
                order_id = str(detail[0])
                product_name = product_name + "," + str(detail[1])
                status = str(detail[3])
                price = str(detail[4])
                delivery_date = str(detail[5])

            return "Your order is {} on {}. You ordered {} products and the total order value was {}".format(status,
                                                                                                             delivery_date,
                                                                                                             product_name,
                                                                                                             price)

    def get_last_order_info(self):
        order_info = sql_connector.get_sql_data(
            '''with cn_order_data as (
                        select order_id,prod_name from consumer.cn_order_data where order_id = (
                        SELECT  max(id) as id from consumer.cn_order where consumer_id ={} )
                    ),cn_order as (
                        select id,status,total_amount,n_slot_id from consumer.cn_order where consumer_id={}
                    )
                    select * from cn_order_data left join cn_order on cn_order_data.order_id=cn_order.id
            '''.format(self.consumer_id, self.consumer_id))
        if order_info:
            status = ''
            total_amount = ''
            n_slot_id = ''
            product_name = ''
            for info in order_info:
                product_name = product_name + " " + info[1]
                status = info[3]
                if status == 'D':
                    status = 'Delivered'
                if status == 'X':
                    status = 'Canceled'
                if status == 'P':
                    status = 'Pending'
                if status == 'RE':
                    status = 'Return state'
                total_amount = info[4]
                n_slot_id = info[5]
            # print(n_slot_id)
            n_slot_id = TM.get_mb_from_yymmdd(n_slot_id)
            ans = "Your order is {} on {}. You ordered {} products and the total order value was {}.".format(status,
                                                                                                             n_slot_id,
                                                                                                             product_name,
                                                                                                             total_amount)
            return ans
        else:
            return "No last order"

    def consumer_history(self):
        consumer_data = sql_connector.get_sql_data('''
            with cn_consumer as(
                select id from consumer.cn_consumer where cn_consumer.phone ={}
            ),ord as(
                select id,total_amount,item_count,n_slot_id,status from consumer.cn_order where consumer_id = (select id from cn_consumer) order by id desc limit 5 
            ),cn_order_data as (
                select id,quantity,prod_name,order_id from consumer.cn_order_data where order_id in (select id from ord )
            )
            select order_id,GROUP_CONCAT(prod_name," quantity: ", quantity ORDER BY prod_name,quantity SEPARATOR ', ') as prod_name,status,n_slot_id  
            from ord left join cn_order_data on ord.id=cn_order_data.order_id group by 1,3,4
        '''.format(self.phone))
        consumer_address = sql_connector.get_sql_data('''
                select google_address from consumer.cn_address where id=(SELECT address_id  from consumer.cn_consumer where cn_consumer.phone ={})
            '''.format(self.phone))
        address = consumer_address[0][0]
        consumer_dict = {}

        for order in consumer_data:
            key = "order_id : {}".format(order[0])
            consumer_dict[key] = {"product_name and quantity : {}".format(order[1]), "status : {}".format(order[2]),
                                  "Delivery date : {}".format(order[3])}

        return "latest order : {}".format(self.get_last_order_info()) + "\n " + str(
            consumer_dict) + "\n consumer_address: {}".format(address)

    def out_context(self):

        result = chain.invoke(
            {"context": self.consumer_history(), "consumer_name": self.consumer_name, "question": self.query})
        return result

    def function_calling(self, name: str):
        try:
            do = f"{name}"
            if hasattr(self, do) and callable(func := getattr(self, do)):
                ans = func()
                return ans
        except:
            return "Sorry i cant help in this moment .Please try another question or contact with the admin"


# print(df.to_string())
#

if __name__ == "__main__":
    cm = Consumer_Manager()
    c = cm.get_consumer_name("7986640195")
    print(cm.get_last_five_order())
