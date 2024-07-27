from managers.consumer_manager import Consumer_Manager

CM = Consumer_Manager


class Agent_connect:

    def __init__(self, phone, question):
        self.phone = phone
        self.question = question

    def agent_chat(self):
        print(self.phone)
        print(self.question)
        api = ""
        return "hi from agent side"
