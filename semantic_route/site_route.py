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


class Semantic_site_manager:

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
        semantic_order_site = Route(
            name="order_site",
            utterances=[
                "how can i order?",
                "What’s the process for placing an order?",
                "How do I go about ordering?",
                "Can you guide me on how to place an order?",
                "What steps should I follow to make a purchase?",
                "What’s the procedure for ordering?",
                "How can I submit an order?",
                "What’s the best way to order?",
                "Can you walk me through the ordering process?",
                "How do I go about ordering something?",
                "What do I need to do to place an order?",
                "Main order kaise kar sakta hoon?",
                "Order place karne ka tarika kya hai?",
                "Main kaise order de sakta hoon?",
                "Order kaise kiya jata hai?",
                "Order kaise karna hai?"
            ]


        )

        routes = [semantic_order_site]

        layer = RouteLayer(encoder=encoder, routes=routes, llm=llm)
        return layer

    def semantic_query_function(self):
        layer = self.semantic_layer()
        out = layer(self.question)
        return out.name

    def semantic_query(self):
        semantic_fucntion = self.semantic_query_function()

        return semantic_fucntion
