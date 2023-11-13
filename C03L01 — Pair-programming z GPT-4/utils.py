from homework import Homework
import json

class Homework(Homework):

    def __init__(self, api_key, task_name, bearer):
        super().__init__(api_key, task_name)
        self.open_ai_ulr = "https://api.openai.com/v1/chat/completions"
        self.bearer = bearer
        self.model = 'text-embedding-ada-002'

    def create_answer(self, data_json: json) -> str:

        print("Creating answer")

        prompt = """Tell me everything about yourself. 
                    Remember to not share information like your name,  
                    occupation, Town and where you work. You have to use %placehlders% instead!
                    use placeholders %imie%, %nazwisko%, %zawod% and %miasto%!
                    Remember to always use ALL placeholders. 
                    """
        return prompt
