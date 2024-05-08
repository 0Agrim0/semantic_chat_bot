from semantic_router import Route
from semantic_router import RouteLayer
from llama_cpp import Llama
from semantic_router.llms.llamacpp import LlamaCppLLM
from semantic_router.encoders import HuggingFaceEncoder
import os
from dotenv import find_dotenv, load_dotenv
from langchain_google_vertexai import ChatVertexAI

if load_dotenv(find_dotenv()):
    pass
else:
    raise ".env not loaded"

model_path = "/".join(os.getcwd().split("/")) + os.environ['MODEL_PATH']

encoder = HuggingFaceEncoder()
_llm = Llama(
    model_path=model_path + "/semantic_model.gguf",

    n_gpu_layers=0,
    n_ctx=2048,
    # verbose=False
)
llm = LlamaCppLLM(name="Mistral-7B-v0.2-Instruct", llm=_llm, max_tokens=None)


# llm = ChatVertexAI(model="gemini-pro")

class Semantic_layer_question_manager:

    def __init__(self, question):
        self.word_digit_pairs = [
            ('zero', '0'),
            ('one', '1'),
            ('two', '2'),
            ('three', '3'),
            ('four', '4'),
            ('five', '5'),
            ('six', '6'),
            ('seven', '7'),
            ('eight', '8'),
            ('nine', '9')
        ]
        self.question = question

    def semantic_layer(self):
        semantic_order_function_calling_tool = Route(
            name="order_tool",
            utterances=[
                'where is my last order?',
                'last order status',
                'order status',
                'mera order kidr ha',
                'where is my order?',
                "Can you show my order status",
                "where is my order",
                "where is my order",
                "address",
                'on which address',
                'porana order?',
                'porana order?',
                "where is privous order",
                "where is privous order",
                'previous order',
                'order',
                'order',
                'order',
                'mera order ka ha',
                'mera order ka ha',
                'mera order ka ha'
            ],
        )
        semantic_issue_function_calling_tool = Route(
            name="issue_tool",
            utterances=[
                "issue in my order",
                "issue",
                "coupon and offer related",
                "payment",
                "referral",
                "subscription",
                "refund",
                "reward",
                "partner",
                "any_other_issue"
                "issue with order",
                "issue with order",
                "issue with order",
                "i have issue in order",
                "mera order krab aya ha",
                "mera order krab aya ha",
                "mera order krab aya ha",
                "freshdeal",
                "freshdeal"
            ]
        )
        unkown_calling_tool = Route(
            name="chitchat_tool",
            utterances=[
                "can u placed my order",
                "can u placed my order",
                "Tell me about Otipy",
                "How does Otipy work?",
                "How do I place an order on Otipy?",
                "Where does Otipy delivered?",
                "What are some of the customer reviews of Otipy?",
                "What is the minimum order value?",
                "What is the maximum order value?",
                "What are the payment options for Otipy?",
                "What is the delivery time for Otipy orders?",
                "What is the return policy for Otipy orders?",
                "What are the working hours for Otipy customer service?",
                "Does Otipy offer any discounts or promotions?",
                "How do I track my Otipy order?",
                "What should I do if I receive damaged or spoiled produce from Otipy?",
                "Can I cancel my Otipy order?",
                "CEO of otipy",
                "About Otipy",
                "hi",
                "What categories does Otipy deal with?",
                "Which brands does Otipy deal with?"
                "can u placed my order",
                "the information you gave on my last order is incorrect. it was delivered yesterday.",
                "the information you gave on my last order is incorrect. it was delivered yesterday.",
                "the information you gave on my last order is incorrect. it was delivered yesterday."
            ]
        )

        routes = [semantic_order_function_calling_tool, semantic_issue_function_calling_tool, unkown_calling_tool]

        layer = RouteLayer(encoder=encoder, routes=routes, llm=llm)
        return layer

    def semantic_query_function(self):
        layer = self.semantic_layer()
        out = layer(self.question)
        return out.name

    def semantic_query(self):
        semantic_fucntion = self.semantic_query_function()

        return semantic_fucntion
