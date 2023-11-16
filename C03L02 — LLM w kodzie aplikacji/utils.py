from homework import Homework
import json
import requests
import time
import openai


class Homework(Homework):

    def __init__(self, api_key: str, task_name: str, bearer: str, retry: int):
        super().__init__(api_key, task_name)
        self.open_ai_ulr = "https://api.openai.com/v1/chat/completions"
        self.bearer = bearer
        self.retry = retry
        self.model = "gpt-3.5-turbo"

    def create_answer(self, data_json: json) -> str:

        print("Creating answer")

        msg = data_json['msg']
        input_url = data_json['input']
        question = data_json['question']

        text = self.read_txt_from_url(input_url, 2)
        answer = self.answer_for_question(msg, text, question)
        return answer

    def read_txt_from_url(self, url: str, wait_before_next_request: int) -> str:

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'
        }

        for i in range(1, self.retry):
            response = requests.get(url, headers=header)

            if response.status_code == 200:
                break
            time.sleep(1 * wait_before_next_request)
            wait_before_next_request *= 2

        return response.text

    def answer_for_question(self, message: str, text: str, question: str):

        print("Creating answer")
        chat_url = 'https://api.openai.com/v1/chat/completions'

        header = {
            "Authorization": f"Bearer {self.bearer}"
        }

        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": f"{message}\n ###Context {text}"
                },
                {
                    "role": "user",
                    "content": f"{question}"
                }
            ]
        }

        result = requests.post(chat_url, json=data, headers=header)

        result_json = json.loads(result.text)

        answer = self.get_answer_from_api_response(result_json)

        return answer
