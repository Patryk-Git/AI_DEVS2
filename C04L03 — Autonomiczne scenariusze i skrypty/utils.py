import requests
from homework import Homework
import json
from uuid import uuid4

class Homework(Homework):

    def __init__(self, api_key, task_name, bearer):
        super().__init__(api_key, task_name)
        self.open_ai_ulr = "https://api.openai.com/v1/chat/completions"
        self.bearer = bearer

    def analyze_picture(self, url: str):

        header = {
            "Authorization": f"Bearer {self.bearer}"
        }

        data = {
            "model": "gpt-4-vision-preview",
            "messages": [
              {
                "role": "user",
                "content": [
                  {
                    "type": "text",
                    "text": """Jeśli na obrazku jest gnow powiedz jakiego koloru jest jego czapka.
                                Natomiast jeśli na obrazku jest coś innego wypisz: ERROR"""
                  },
                  {
                    "type": "image_url",
                    "image_url": {
                      "url": f"{url}"
                    }
                  }
                ]
              }
            ],
            "max_tokens": 300
        }

        result = requests.post(self.open_ai_ulr, json=data, headers=header)

        result_json = json.loads(result.text)

        print(result_json)

        print("Answer created")

        return result_json['choices'][0]['message']['content']
