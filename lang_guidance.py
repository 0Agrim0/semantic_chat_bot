from guidance import models, gen, select
from dotenv import find_dotenv, load_dotenv
import os

if load_dotenv(find_dotenv()):
    pass
else:
    raise ".env not loaded"

path = "/".join(os.getcwd().split("/")) + os.environ['MODEL_PATH'] + "/semantic_model.gguf"
print(path)
# load a model (could be Transformers, LlamaCpp, VertexAI, OpenAI...)
llama2 = models.LlamaCpp(path)


# @guidance
def laguage_detector(query):
    question = "what is the language of the following text."
    language = ['English', 'Hindi', 'Hinglish']
    lm = llama2 + f"{question}: {query}\n"
    # append text or generations to the model
    lm += 'Answer: ' + select(language)
    return lm

if __name__=="__main__":
   a= laguage_detector("hello")
   print(a)
