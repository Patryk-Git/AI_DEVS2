from utils import Homework

from dotenv import load_dotenv
import os

TASK_NAME = 'knowledge'

if __name__ == "__main__":
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")

    devs = Homework(API_KEY, TASK_NAME, OPEN_AI_KEY)
    data = devs.get_task()
    question = data['question']
    print(question)
    case = devs.check_question(question)

    if case == 1:


