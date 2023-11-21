import requests
from homework import Homework
import json
from uuid import uuid4


class Homework(Homework):

    def __init__(self, api_key, task_name, bearer):
        super().__init__(api_key, task_name)
        self.open_ai_ulr = "https://api.openai.com/v1/chat/completions"
        self.bearer = bearer
        self.model = 'text-embedding-ada-002'

    def create_embedding(self, data_str: str) -> json:
        embedding_url = 'https://api.openai.com/v1/embeddings'

        print('Creating embedding')

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

    def create_answer(self, data: str, question: str) -> str:
        print("Creating answer")

        header = {
            "Authorization": f"Bearer {self.bearer}"
        }

        data = {
            "messages": [{'role': 'system',
                          'content': f'Odpowiedz na pytanie użytkownika na podstawie tego dokumentu: {data}'},
                         {'role': 'user', 'content': question}],
            'model': 'gpt-3.5-turbo'
        }

        result = requests.post(self.open_ai_ulr, json=data, headers=header)

        result_json = json.loads(result.text)
        answer = self.get_answer_from_api_response(result_json)

        print(answer)

        print("Answer created")

        return answer

    def read_json(self, json_path: str) -> str:
        with open(json_path) as user_file:
            parsed_json = json.load(user_file)
        return parsed_json

    def create_documents(self, json_data: json, collection_name: str) -> list:
        documents_with_meta = []
        for record in json_data:
            document_with_meta = [
                {
                    'source': collection_name,
                    'content': f""" IMIE:  {record['imie']}, NAZWISKO: {record['nazwisko']}, WIEK: {record['wiek']},
                                O MNIE: {record['o_mnie']}, 
                                ULUBIONA POSTAC Z KAPITANA BOMBY: {record['ulubiona_postac_z_kapitana_bomby']},
                                ULUBIONY SERIAL: {record['ulubiony_serial']}, ULUBIONY FILM: {record['ulubiony_film']},
                                ULUBIONY KOLOR:  {record['ulubiony_kolor']}
                                """,
                    'uuid': str(uuid4())
                }
            ]
            documents_with_meta.append(document_with_meta)
        return documents_with_meta
