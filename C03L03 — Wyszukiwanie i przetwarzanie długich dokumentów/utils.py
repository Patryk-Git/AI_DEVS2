import requests
from homework import Homework
import json


class Homework(Homework):

    def __init__(self, api_key, task_name, bearer):
        super().__init__(api_key, task_name)
        self.open_ai_ulr = "https://api.openai.com/v1/chat/completions"
        self.bearer = bearer
        self.model = "gpt-4"

    def create_answer(self, data_list: list):

        print(data_list)
        answer = self.answer_for_question(data_list)

        return answer
    def answer_for_question(self, hints: str):
        print("Creating answer")
        chat_url = 'https://api.openai.com/v1/chat/completions'

        header = {
            "Authorization": f"Bearer {self.bearer}"
        }
        system_content = f"""Twoim zadaniem jest odgadnięcie osobo o któej mówi użytkownik. 
                            Użytkownik będzie podawał kolejne podpowiedzi. Jeśli nie wiesz odpowiadasz 'Nie wiem' a jeśli 
                            wiesz podaj tylko imię i nazwisko
                        """
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_content
                },
                {
                    "role": "user",
                    "content": f"Kim jestem? Podpowoedzi {hints}"
                }
            ]
        }

        result = requests.post(chat_url, json=data, headers=header)

        result_json = json.loads(result.text)

        answer = self.get_answer_from_api_response(result_json)

        return answer
