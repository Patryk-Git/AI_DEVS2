from utils import Homework

from dotenv import load_dotenv
import os

TASK_NAME = 'tools'

if __name__ == "__main__":
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")

    devs = Homework(API_KEY, TASK_NAME, OPEN_AI_KEY)
    data = devs.get_task()
    user_content = data['question']
    answer = devs.answer_for_question(user_content)
    devs.submit_homework(answer)
