import requests
from homework import Homework
import json
import logging


class Homework(Homework):

    def __init__(self, api_key, task_name, bearer):
        super().__init__(api_key, task_name)
        self.open_ai_ulr = "https://api.openai.com/v1/chat/completions"
        self.bearer = bearer
        self.model = 'text-embedding-ada-002'

    def create_answer(self, data_str: str):
        print("Creating answer")
        embedding_url = 'https://api.openai.com/v1/embeddings'

        header = {
            "Authorization": f"Bearer {self.bearer}"
        }
        data = {
            "input": data_str,
            'model': self.model
        }

        result = requests.post(embedding_url, json=data, headers=header)

        result_json = json.loads(result.text)

        return result_json
