from semantic_router import Route
from semantic_router import RouteLayer
from llama_cpp import Llama
from semantic_router.llms.llamacpp import LlamaCppLLM
from semantic_router.encoders import HuggingFaceEncoder
import os
from dotenv import find_dotenv, load_dotenv

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


class Semantic_layer_order_manager:

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
            name="get_last_order_info",
            utterances=[
                'where is my last order?',
                'last order status',
                'order status',
                'mera order kidr ha',
                'where is my order?',
                "Can you show my order status",
                "mera order ka ha",
                "where is my order ?",
                "where is my order ?",
                "where is my order ?",
                "where is my last order?",
                "Last order status",
                "Order ka status kya hai?",
                "Last order ka status kya hai?",
                "Mera last order kahan hai?",
                "mera order ka ha?",
                "mera order ka ha?"
            ],
        )
        semantic_route_get_last_five_order = Route(
            name="get_last_five_order",
            utterances=[
                "mera porana order ka ha",
                "mera porana order ka ha",
                "mera porana order ka ha",
                "where is my previos order",
                "where is my previos order",
                "where is my previos order",
                "where is my previos order",
                'where is my previous order?',
                'previous order',
                'porana order',
                'first order?',
                'where is my first order',
                'day before yesterday order?',
                'second last order?',
                'porana order?',
                'porana order?',
                'where is my previous order?',
                'where is my previous order?',
                'where is my prvious order?',
                "Purana order kaha hai?",
                "Purane order ka kya haal hai?",
                "Kya purane order pending hain?",
                "Purane order ki sthiti kya hai?",
                "Purane order ka update milega?",
                "Second last order?",
                "Day before yesterday order?",
                "Where is my first order?",
                "Parson ka order?",
                "porana order ka ha",
                "porana order ka ha"
            ],
        )

        out_context = Route(
            name="out_context",
            utterances=[
                "order id 2413",
                "order id",
                "order id 41341",
                "where is my order with this order id 16022951",
                "where is my order with this order id 16022951",
                "where is my order with cancel order",
                "order id 4134",
                "order id14234"
            ]
        )

        routes = [semantic_order_function_calling_tool, semantic_route_get_last_five_order, out_context]

        layer = RouteLayer(encoder=encoder, routes=routes, llm=llm)
        return layer

    def semantic_query_function(self):
        layer = self.semantic_layer()
        out = layer(self.question)
        return out.name

    def semantic_query(self):
        semantic_fucntion = self.semantic_query_function()

        return semantic_fucntion
