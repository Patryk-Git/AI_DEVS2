from utils import Homework
from qdrant import Quadrant

from dotenv import load_dotenv
import os


TASK_NAME = 'search'
COLLECTION_NAME = 'AI_DEVS'
COLLECTION_SIZE = 1536

if __name__ == "__main__":
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")

    quadrant = Quadrant(COLLECTION_NAME)
    devs = Homework(API_KEY, TASK_NAME, OPEN_AI_KEY, 5)
    data = devs.get_task()
    question_embeding = devs.create_embedding(data['question'])
    json_data = devs.read_json()
    quadrant.create_collection(COLLECTION_SIZE)

    collection_info = quadrant.get_collectionn()

    if not collection_info.points_count:
        print("Creating documents")
        documents_with_meta = devs.create_documents(json_data)

        points = []
        for document in documents_with_meta[:300]:
            embedding = devs.create_embedding(document[0]['content'])
            points.append({
                'id': document[0]['uuid'],
                'payload': document[0],
                'vector': embedding
            })

        quadrant.upsert_to_collection(points)
    else:
        print("Collection not empty")
    print("Searching")
    print(question_embeding)
    print(data['question'])
    search = quadrant.search(question_embeding)
    answer = search[0].payload.get('url', None)
    devs.submit_homework(answer)
