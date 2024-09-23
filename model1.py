from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat

chat = GigaChat(credentials = 'YTg1ZWYzZmItNDJmYi00ZmNmLWJlMzItN2ZhMTJkNGQ4NmZjOmRjOTI0YjRkLThjOGMtNDlkYy05MmI4LTAyNWNlZDRjZTBmNA==', verify_ssl_certs = False, model="GigaChat-Plus")

class Chat:
    def __init__(self):
        self.messages = []

    def start_chat(self, prompt):
        self.messages = [SystemMessage(content=prompt)]

    def add_message(self, user_input):
        self.messages.append(HumanMessage(content=user_input))

    def get_answer(self):
        res = chat(self.messages)
        self.messages.append(res)
        return res.content
