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
        data = self.find_data(data_json)
        question = data_json['question']
        header = {
            "Authorization": f"Bearer {self.bearer}"
        }
        data = {
            "messages": [{'role': 'system',
                          'content': f'Odpowiedz na pytanie {question}, na bazie dokumentu: {data}'}],
            'model': 'gpt-3.5-turbo'
        }

        result = requests.post(self.open_ai_ulr, json=data, headers=header)

        result_json = json.loads(result.text)
        content = self.get_answer_from_api_response(result_json)

        print(content)

        print("Answer created")

        return content

    def find_data(self, api_json: json) -> list:

        msg = api_json['input']
        question = api_json['question']

        correct_names_data = []
        possible_names = []

        for record in msg:
            possible_names.append(record.split(" ")[0])

        name = [name for name in possible_names if name in question][0]

        for record in msg:
            if name in record:
                correct_names_data.append(record)

        return correct_names_data
