import requests
from homework import Homework
import json
import openai



class Homework(Homework):

    def __init__(self, api_key, task_name, bearer):
        super().__init__(api_key, task_name)
        self.open_ai_ulr = "https://api.openai.com/v1/chat/completions"
        self.bearer = bearer

    def get_exchange_rate(self, currency: str):
        url = f"http://api.nbp.pl/api/exchangerates/tables/A/{currency}/last/"

        response = requests.get(url)

        return json.loads(response.text)

    def get_population(self, country: str):

        ulr = f"https://restcountries.com/v3.1/name/{country}?fields=name,population"

        response = requests.get(url=ulr)

        return json.loads(response.text)

    def general_question(self, question: str):

        header = {
            "Authorization": f"Bearer {self.bearer}"
        }
        data = {
            "messages": [{'role': 'system',
                          'content': "Answer for questions"},
                         {'role': 'user', 'content': question}],
            'model': 'gpt-3.5-turbo'
        }

        result = requests.post(self.open_ai_ulr, json=data, headers=header)

        result_json = json.loads(result.text)
        answer = self.get_answer_from_api_response(result_json)

        return answer

    def ask_model(self, user_content):
        functions = [
            {
                "name": "get_population",
                "description": "gets current population of the given currency",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "country": {"type": "string", "description": "country code required for population info"},
                    }
                },
                "required": ["country"]
            },
            {
                "name": "get_exchange_rate",
                "description": "gets current exchange rate of the given currency to fixed default currency",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "currency": {"type": "string", "description": "country code required for population info"},
                    },
                    "required": ["currency"]
                },
            },
            {
                "name": "general_question",
                "description": "Get answer for general question",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "test": {"type": "string", "description": "a general question"},
                    },
                    "required": ["test"]
                },
            }
        ]
        prompt = (
            """You will be asked questions about a population of a given country, exchange rate of a given currency
            and general question. Pick the correct function
            For currency use currency symbol according to ISO 4217""")

        header = {
            "Authorization": f"Bearer {self.bearer}"
        }
        data = {
            "messages": [{'role': 'system',
                          'content': prompt},
                         {'role': 'user', 'content': user_content}],
            "functions": functions,
            'model': 'gpt-4'
        }

        result = requests.post(self.open_ai_ulr, json=data, headers=header)

        result_json = json.loads(result.text)
        answer = self.get_answer_from_api_response(result_json)

        return answer

    def create_answer(self, data_json: json, question: str):

        if data_json['name'] == 'general_question':
            answer = self.general_question(question)['choices'][0]['message']['content']
            print(answer)
            return answer
        elif data_json['name'] == "get_population":
            print(data_json['arguments']['country'])
            population = self.get_population(data_json['arguments']['country'])
            print(population)
            return population
        elif data_json['name'] == "get_exchange_rate":

            exchange_rate = self.get_population(data_json['arguments']['currency'])
            print(exchange_rate)
            return exchange_rate


