from utils import Homework

from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")

    devs = Homework(API_KEY, "blogger", OPEN_AI_KEY)
    data = devs.get_task()
    answer = devs.create_answer(data)
    devs.submit_homework(answer)
