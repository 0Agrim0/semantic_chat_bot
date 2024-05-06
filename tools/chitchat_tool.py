import os
from lib.sql_connector import get_sql_dataframe
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.document_loaders import DataFrameLoader
from langchain.vectorstores import Chroma
from chromadb.config import Settings
from langchain_core.output_parsers import StrOutputParser
import chromadb
import json
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_vertexai import ChatVertexAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from managers.consumer_manager import Consumer_Manager

CM = Consumer_Manager()

gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv('GOOGLE_AI_CREDENTIALS')
PROJECT_ID = os.getenv('PROJECT_ID')
persist_directory = os.getenv('PERSIST_DIRECTORY')

if persist_directory is None:
    raise Exception("Please set the PERSIST_DIRECTORY environment variable")

# Define the Chroma settings
CHROMA_SETTINGS = Settings(
    persist_directory=persist_directory,
    anonymized_telemetry=False
)
chroma_client = chromadb.PersistentClient(settings=CHROMA_SETTINGS, path=persist_directory)

db = Chroma(persist_directory=persist_directory, embedding_function=gemini_embeddings,
            client_settings=CHROMA_SETTINGS,
            client=chroma_client)
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 1})

llm = ChatVertexAI(model="gemini-pro")

template = """
        You are the Otipy chat bot which help the {consumer_name} to answer the question about Otipy company and where is my order ,where is my previous order 
        Please use the context to provide the simple sweet answer. if context is empty or not related to the question
        just say 'Sorry i cant help'.Please do not mention as provide context.
        Please add username in answer when needed 
        You have only last five order information. if order id is not find in user history do not respond. 
        
        user history :
            {consumer_history}
        
        context:{context}
        
        username: {consumer_name}
        question: {question}
        
        Answer:
        
        IMPORTANT :
            Do not answer question which is not related to the context or out of context just say 'Sorry i cant help you'.
            DO not ask any question to the user.
            Do not explain why you not give answer just say 'Sorry i cant help you'.
            DO not give any fake order status information.
       """
custom_rag_prompt = ChatPromptTemplate.from_template(template)

chain = (
        {
            "context": itemgetter("question") | retriever,
            "consumer_history": itemgetter("consumer_history"),
            "consumer_name": itemgetter("consumer_name"),
            "question": itemgetter("question"),
        }
        | custom_rag_prompt
        | llm
        | StrOutputParser()
)


def read_prompt():
    prompt_path = os.environ.get('PROMPT_PATH')
    with open(os.path.join(prompt_path, "chat_template.txt"), "r+") as file:
        chatbot_template = file.read()
    return chatbot_template


def sql_state():
    f = open('sql_state.json')
    data = json.load(f)
    return data


def sql_state_write( last_enrty_time):
    data = sql_state()
    data['entry_time'] = str(last_enrty_time)
    with open("sql_state.json", "w") as json_file:
        json.dump(data, json_file, indent=2)


def vector_loader():
    state = sql_state()
    if state['entry_time'] == '0':
        sql = "SELECT prompt,response,entry_time FROM chatbot.chatLog where entry_time>{}".format(
            state['entry_time'])
    else:
        sql = "SELECT prompt,response,entry_time FROM chatbot.chatLog where entry_time>'{}'".format(
            state['entry_time'])
    data = get_sql_dataframe(sql)

    load_data = data[['prompt', 'response']]
    # print(data)
    df_loader = DataFrameLoader(load_data, page_content_column="prompt")

    # loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_documents(df_loader.load())

    db = Chroma.from_documents(
        documents=texts,  # Data
        embedding=gemini_embeddings,  # Embedding model
        persist_directory=persist_directory  # Directory to save data
    )

    last_entry_time = data['entry_time'].tail(1).values[0]
    sql_state_write(last_entry_time)
    print('done')


def vecttor_retriever():
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 1})
    return retriever


def vector_query(query):
    chroma_client = chromadb.PersistentClient(settings=CHROMA_SETTINGS, path=persist_directory)
    db = Chroma(persist_directory=persist_directory, embedding_function=gemini_embeddings,
                client_settings=CHROMA_SETTINGS,
                client=chroma_client)
    # retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    docs = db.similarity_search(query, k=10)
    print(chroma_client)
    print(docs)


def rag_query( query, phone):
    try:
        consumer_name = CM.get_consumer_name(phone)
        consumer_history = CM.consumer_history()
        result = chain.invoke({"consumer_history": consumer_history, "consumer_name": consumer_name, "question": query})

        return result

    except:
        consumer_name = CM.get_consumer_name(phone)
        return "I'm sorry {}, but I can't answer your question based on the provided question.".format(consumer_name)

# #
# if __name__ == "__main__":
#     # vector_query("which product otipy sell")
#     # print(a)
#     a = rag_query("which product otipy sell", "agrim")
#     print(a)
