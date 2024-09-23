import requests

CHAD_API_KEY = 'chad-b345d118b07c485c998bf14b2129deadvkulnyzm'

class Chat:
    def __init__(self):
        self.message = None
        self.history = []

    def start_chat(self, prompt):
        self.history = [
            {"role": "system",
            "content": prompt}
            ]

    def add_message(self, user_input):
        self.message = user_input

    def get_answer(self):
        request_json = {
            "message": self.message,
            "api_key": CHAD_API_KEY,
            "history": self.history
        }
        response = requests.post(url='https://ask.chadgpt.ru/api/public/gpt-4o-mini',
                                 json=request_json)
        resp_json = response.json()
        answer = resp_json['response']
        self.history.append(
            {
                "role": "user",
                "content": self.message
            }
        )
        self.history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )
        return answer

    def get_words_count(self):
        pass