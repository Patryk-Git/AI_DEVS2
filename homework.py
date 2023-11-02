import requests
import json
import logging

class Homework:

    def __init__(self, api_key: str, task_name: str) -> None:
        self.token = None
        self.api_key = api_key
        self.task_name = task_name
        self.ai_devs_url = f"https://zadania.aidevs.pl/token/{task_name}"


    def get_task(self) -> json:
        print("Getting task")
        url = self.ai_devs_url

        data = {
            "apikey": self.api_key
        }
        token_json = requests.post(url=url, json=data)

        response_dict = json.loads(token_json.text)
        token = response_dict["token"]


        self.token = token
        url = f"https://zadania.aidevs.pl/task/{token}"

        auth = requests.get(url)
        json_output = json.loads(auth.text)
        with open("context.json", "w") as outfile:
            json.dump(json_output, outfile)

        print(json_output)

        return json_output


    def submit_homework(self, answer: json):
        print("Submitting homework")
        url = f"https://zadania.aidevs.pl/answer/{self.token}"

        answer_json = {
            'answer': answer
        }

        result = requests.post(url=url, json=answer_json)

        print(result.text)

    def get_answer_from_api_response(self, api_json: json):

        result = api_json['choices'][0]
        content = result['message']['content']

        return content

