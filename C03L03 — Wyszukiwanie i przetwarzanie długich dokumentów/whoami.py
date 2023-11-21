from utils import Homework
import re
from dotenv import load_dotenv
import os

TASK_NAME = 'whoami'

if __name__ == "__main__":
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")
    devs = Homework(API_KEY, TASK_NAME, OPEN_AI_KEY)

    hints = []
    while True:
        data = devs.get_task()
        hints.append(data['hint'])
        answer = devs.create_answer(hints)
        print(answer)
        if answer != 'Nie wiem':
            print(answer)
            break
    devs.submit_homework(answer)
