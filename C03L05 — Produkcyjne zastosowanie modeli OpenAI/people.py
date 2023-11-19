from utils import Homework
from qdrant import Quadrant

from dotenv import load_dotenv
import os

TASK_NAME = 'people'
COLLECTION_NAME = 'C03L05'
COLLECTION_SIZE = 1536

if __name__ == "__main__":
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")

    quadrant = Quadrant(COLLECTION_NAME)
    devs = Homework(API_KEY, TASK_NAME, OPEN_AI_KEY)
    data = devs.get_task()
    json_data = devs.read_json('people.json')
    question = data['question']

    question_embedding = devs.create_embedding(question)

    quadrant.create_collection(COLLECTION_SIZE)

    collection_info = quadrant.get_collectionn()

    if not collection_info.points_count:
        print("Creating documents")
        documents_with_meta = devs.create_documents(json_data, COLLECTION_NAME)

        print(documents_with_meta)

        points = []
        for document in documents_with_meta:
            embedding = devs.create_embedding(document[0]['content'])
            points.append({
                'id': document[0]['uuid'],
                'payload': document[0],
                'vector': embedding
            })

        quadrant.upsert_to_collection(points)
    else:
        print("Collection not empty")

    search = quadrant.search(question_embedding)

    content = search[0].payload.get('content', None)

    answer = devs.create_answer(content, question)
    devs.submit_homework(answer)