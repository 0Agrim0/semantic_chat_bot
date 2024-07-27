from guidance import models, gen, select
from dotenv import find_dotenv, load_dotenv
import os
import json

if load_dotenv(find_dotenv()):
    pass
else:
    raise ".env not loaded"

path = "/".join(os.getcwd().split("/")) + os.environ['MODEL_PATH'] + "/semantic_model.gguf"

llm = models.LlamaCpp(path)


# @guidance
def laguage_detector(query):
    question = "what is the language of the following text."
    language = ['English', 'Hindi', 'hinglish']
    lm = llm + f"{question}: {query}\n"
    # append text or generations to the model
    lm += f"""{{
            "text":"{query}",
            "language":"{select(language, name='language')}"}}"""
    return lm



