import requests
from homework import Homework
import json
import logging

class Homework(Homework):

    def __init__(self, api_key, task_name, bearer):
        super().__init__(api_key, task_name)
        self.open_ai_ulr = "https://api.openai.com/v1/chat/completions"
        self.bearer = bearer

    def create_answer(self, data_json: json) -> str:

        print("Creating answer")
        blog = data_json['blog']

        header = {
            "Authorization": f"Bearer {self.bearer}"
        }
        data = {
            "messages": [{'role': 'system',
                          'content': 'Jeste blogerem. Masz napisać po kilka zdań do każdego z tematów podanych w tablicy. Zwróć odpowiedź w formacie json {answer: [wpis_1, wpis_2, itd]'},
                         {'role': 'user', 'content': str(blog)}],
            'model': 'gpt-3.5-turbo'
        }

        result = requests.post(self.open_ai_ulr, json=data, headers=header)

        result_json = json.loads(result.text)
        content = self.get_answer_from_api_response(result_json)

        print(content)

        print("Answer created")

        return content
