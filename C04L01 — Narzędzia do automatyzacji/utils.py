import requests
from homework import Homework
import json
import openai


def get_exchange_rate(currency: str):
    url = f"http://api.nbp.pl/api/exchangerates/tables/A/{currency}/last/"

    response = requests.get(url)

    return json.loads(response.text)["rates"][0]["mid"]
class Homework(Homework):

    def __init__(self, api_key, task_name, bearer):
        super().__init__(api_key, task_name)
        self.open_ai_ulr = "https://api.openai.com/v1/chat/completions"
        self.bearer = bearer



    def ask_model(self, user_content):
        functions = [
            {
                "name": "get_exchange_rate",
                "description": "gets current exchange rate of the given currency to fixed default currency",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "currency": {"type": "string", "description": "currency for which exchange rate is required"},
                    },
                    "required": ["currency"]
                },
            },
            {
                "name": "general_question",
                "description":
                    "a function returning answer to general question not related to exchange rates and countries' populations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string", "description": "a general question"},
                    },
                    "required": ["question"]
                },
            }
        ]
        prompt = (
            "You will be asked questions about a population of a given country, exchange rate of a given currency "
            "and other general question. For country name use English name only. "
            "For currency use currency symbol according to ISO 4217. For general questions use the same language.")

        header = {
            "Authorization": f"Bearer {self.bearer}"
        }
        user_content = 'Jaki jest kurs dolara'
        data = {
            "messages": [{'role': 'system',
                          'content': prompt},
                         {'role': 'user', 'content': user_content}],
            "functions": functions,
            'model': 'gpt-3.5-turbo'
        }

        result = requests.post(self.open_ai_ulr, json=data, headers=header)

        result_json = json.loads(result.text)
        answer = self.get_answer_from_api_response(result_json)

        return answer

