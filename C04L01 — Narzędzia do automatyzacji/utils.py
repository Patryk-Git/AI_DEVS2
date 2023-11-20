import requests
from homework import Homework
import json
import openai


class Homework(Homework):

    def __init__(self, api_key, task_name, bearer):
        super().__init__(api_key, task_name)
        self.open_ai_ulr = "https://api.openai.com/v1/chat/completions"
        self.bearer = bearer

    def get_currency(self):
        url = "http://api.nbp.pl/api/exchangerates/tables/A/"

        response = requests.get(url)

        return response.text

    def ask_model(self, system_content: str = None, user_content: str = None):
        header = {
            "Authorization": f"Bearer {self.bearer}"
        }

        data = {
            "messages": [{'role': 'system',
                          'content': system_content},
                         {'role': 'user', 'content': user_content}],
            'model': 'gpt-3.5-turbo'
        }

        result = requests.post(self.open_ai_ulr, json=data, headers=header)

        result_json = json.loads(result.text)
        answer = self.get_answer_from_api_response(result_json)

        return answer

    def check_question(self, question: str):
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_currency",
                    "description": "Get the currency",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "format": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"],
                                "description": "The temperature unit to use. Infer this from the users location.",
                            },
                        },
                        "required": ["location", "format"],
                    },
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_n_day_weather_forecast",
                    "description": "Get an N-day weather forecast",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "format": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"],
                                "description": "The temperature unit to use. Infer this from the users location.",
                            },
                            "num_days": {
                                "type": "integer",
                                "description": "The number of days to forecast",
                            }
                        },
                        "required": ["location", "format", "num_days"]
                    },
                }
            },
        ]

        answer = self.ask_model(system_content, question)

        return answer

