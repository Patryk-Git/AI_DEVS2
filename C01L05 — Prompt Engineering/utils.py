import requests
from homework import Homework
import json
import logging

class Homework(Homework):

    def __init__(self, api_key, task_name, bearer):
        super().__init__(api_key, task_name)
        self.open_ai_ulr = "https://api.openai.com/v1/chat/completions"
        self.bearer = bearer

    def create_answer(self, question:str) -> json:

        print("Creating answer")

        data = {
            "question": question,
        }

        url = f"https://zadania.aidevs.pl/task/{self.token}"
        result = requests.post(url, data=data)

        result_json = json.loads(result.text)
        answer = result_json['answer']

        answer = self.guardrails(question=question, answer=answer)

        return answer

    def guardrails(self, question: str, answer: str) -> str:

        header = {
            "Authorization": f"Bearer {self.bearer}"
        }
        data = {
            "messages": [{'role': 'system',
                          'content': """You are going to get auestion and answer. You have to verify if the answer for 
                          the question is true. If it's true return 'Yes' if it's not true return 'No' """},
                         {'role': 'user', 'content': f"Question: {question}, answer: {answer}"}],
            'model': 'gpt-3.5-turbo'
        }

        result = requests.post(self.open_ai_ulr, json=data, headers=header)
        result_json = json.loads(result.text)
        result = result_json['choices'][0]
        print(result)
        content = result['message']['content']
        print(content)
        print("Answer created")

        return content
