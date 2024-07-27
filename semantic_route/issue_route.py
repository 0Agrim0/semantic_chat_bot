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


class Semantic_layer_issue_manager:

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
        semantic_coupon = Route(
            name="coupon",
            utterances=[
                "coupon and offer related "
                "कूपन",
                "wallet",
                "wallet",
                "coupon mai issue ha",
                "wallet"
            ],
        )
        semantic_payment= Route(
            name="payment",
            utterances=[
                "payment",
                "mera payment thick sa nahi ho bhai"
                "bhugataan",
                "bhugataan"
                "payment",
                "payment"
            ],
        )
        semantic_freshdaily = Route(
            name="freshdaily",
            utterances=[
                "freshdaily "
            ],
        )
        semantic_referral = Route(
            name="referral",
            utterances=[
                "referral"
            ],

        )
        out_subscription = Route(
            name="subscription",
            utterances=[
                "subscription",
                "subscription ka order nahi aya"
            ]
        )
        out_refund = Route(
            name="refund",
            utterances=[
                "refund",
                "merko refund chaiya"
            ]
        )
        out_reward = Route(
            name="reward",
            utterances=[
                "reward"
            ]
        )
        out_partner = Route(
            name="partner",
            utterances=[
                "partner"
            ]
        )
        out_any_other_issue = Route(
            name="any_other_issue",
            utterances=[
                "any_other"
            ]

        )
        default = Route(
            name="default",
            utterances=[
                "meri sbji krab ai ha",
                "meri sbji krab ai ha",
            ]
        )
        routes = [default,semantic_coupon, semantic_payment,semantic_freshdaily, semantic_referral,out_subscription,out_refund,out_reward,out_partner,out_any_other_issue]

        layer = RouteLayer(encoder=encoder, routes=routes, llm=llm)
        return layer

    def semantic_query_function(self):
        layer = self.semantic_layer()
        out = layer(self.question)
        return out.name

    def semantic_query(self):
        semantic_fucntion = self.semantic_query_function()

        return semantic_fucntion
