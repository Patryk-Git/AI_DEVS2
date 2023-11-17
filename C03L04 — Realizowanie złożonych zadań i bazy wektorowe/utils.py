import requests
from homework import Homework
import json
from uuid import uuid4

class Homework(Homework):

    def __init__(self, api_key, task_name, bearer, retry):
        super().__init__(api_key, task_name)
        self.open_ai_ulr = "https://api.openai.com/v1/chat/completions"
        self.bearer = bearer
        self.model = 'text-embedding-ada-002'
        self.retry = retry

    def create_embedding(self, data_str: str) -> json:
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



        return result_json['data'][0]['embedding']

    def create_answer(self, data_json: json) -> str:
        print("Creating answer")

        msg = data_json['msg']
        input_url = data_json['input']
        question = data_json['question']

        text = self.read_json(input_url, 2)
        # return answer

    def read_json(self) -> str:
        with open('archiwum.json') as user_file:
            parsed_json = json.load(user_file)
        return parsed_json

    def create_documents(self, json_data: json) -> list:

        documents_with_meta = []

        for record in json_data:
            document_with_meta = [
                {
                    'source': 'test',
                    'title': record['title'],
                    'content': record['info'],
                    'url': record['url'],
                    'uuid': str(uuid4())
                }
            ]
            documents_with_meta.append(document_with_meta)
        return documents_with_meta
