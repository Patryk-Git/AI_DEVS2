import requests
from homework import Homework
import json
from uuid import uuid4

class Homework(Homework):

    def __init__(self, api_key, task_name, bearer):
        super().__init__(api_key, task_name)
        self.open_ai_ulr = "https://api.openai.com/v1/chat/completions"
        self.bearer = bearer
        self.model = "gpt-3.5-turbo"

    def answer_for_question(self, user_content: str):
        print("Creating answer")

        header = {
            "Authorization": f"Bearer {self.bearer}"
        }

        system_content = """Decide whether the task should be added to the ToDo list or to the calendar 
                            (if time is provided) and return the corresponding JSON
                            ###Context '''
                            Example for ToDo:
                            Napisz API = {"tool": "Napisz API", "desc" : "Napisz API"}
                            Przypomnij mi, że mam kupić mleko = {"tool":"ToDo","desc":"Kup mleko" }
                            
                            Example for Calendar:
                            Jutro mam spotkanie z Marianem = {"tool":"Calendar","desc":"Spotkanie z Marianem","date":"2023-11-24"}
                            W niedzielę muszę kupić wode = {"tool":"Calendar","desc":"Kupic wode","date":"2023-11-26"}
                            Za dwa dni muszę napisać 5 stron wypracowania = {"tool":"Calendar","desc":"Napisz wypracowanie","date":"2023-11-25"}
                            
                            Today's date = 2023-11-24
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
                    "content": f"{user_content}"
                }
            ]
        }

        result = requests.post(self.open_ai_ulr, json=data, headers=header)

        result_json = json.loads(result.text)

        answer = self.get_answer_from_api_response(result_json)

        return json.loads(answer)