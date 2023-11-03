import requests
from homework import Homework
import json
import openai
import pathlib

class Homework(Homework):

    def __init__(self, api_key, task_name, bearer):
        super().__init__(api_key, task_name)
        self.open_ai_ulr = "https://api.openai.com/v1/chat/completions"
        self.bearer = bearer
        self.model = 'text-embedding-ada-002'

    def create_answer(self, file_path: pathlib.Path) -> str:
        print("Creating answer")
        openai.api_key = self.bearer
        audio_file = open(file_path, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

        return transcript['text']
