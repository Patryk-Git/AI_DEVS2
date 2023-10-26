import requests
import homework
import json


class HOMEWORK:

    def __init__(self, api_key: str, task_name: str) -> None:
        self.api_key = api_key
        self.task_name = task_name
        self.ai_devs_url = f"https://zadania.aidevs.pl/token/{task_name}"

    def get_task(self) -> str:
        url = self.ai_devs_url

        data = {
            "apikey": self.api_key
        }
        token_json = requests.post(url=url, json=data)

        response_dict = json.loads(token_json.text)
        token = response_dict["token"]

        url = f"https://zadania.aidevs.pl/task/{token}"

        auth = requests.get(url)
        print(auth.text)

        return auth.text


def submit_homework(api_key: str, task_name: str):
    url = f"https://zadania.aidevs.pl/token/{task_name}"

    data = {
        "apikey": api_key
    }
    token_json = requests.post(url=url, json=data)

    print(token_json)

    response_dict = json.loads(token_json.text)
    token = response_dict["token"]

    url = f"https://zadania.aidevs.pl/task/{token}"

    auth = requests.get(url)

    print(auth.text)

    response_dict = json.loads(auth.text)
    print(response_dict['input'])

    url = "https://api.openai.com/v1/moderations"

    header = {
        "Authorization": "Bearer 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"
    }
    data = {
        "input": response_dict['input']

    }
    auth = requests.post(url, json=data, headers=header)
    a = json.loads(auth.text)
    b = []
    for i in range(len(response_dict['input'])):

        result = a['results'][i]['flagged']
        print(result)
        if result:
            b.append(1)
        else:
            b.append(0)

    answer = {
        "answer": b
    }
    print(answer)

    url = f"https://zadania.aidevs.pl/answer/{token}"

    result = requests.post(url=url, json=answer)

    print(result.text)


def get_task(api_key: str, task_name: str):
    url = f"https://zadania.aidevs.pl/token/{task_name}"

    data = {
        "apikey": api_key
    }
    token_json = requests.post(url=url, json=data)

    print(token_json)

    response_dict = json.loads(token_json.text)
    token = response_dict["token"]

    url = f"https://zadania.aidevs.pl/task/{token}"

    auth = requests.get(url)

    print(auth.text)
