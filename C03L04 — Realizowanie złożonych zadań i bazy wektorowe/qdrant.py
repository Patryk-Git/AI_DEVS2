from dotenv import load_dotenv
import os
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, Distance, VectorParams, PointStruct
from qdrant_client import QdrantClient
from qdrant_client.http import models

class Quadrant():
    def __init__(self, collection_name: str) -> None:
        load_dotenv()
        self.ulr = os.getenv("QDRANT_URL")
        self.client = QdrantClient(self.ulr, timeout=1000000)
        self.collection_name = collection_name

    def get_collectionn(self):

        collections = self.client.get_collection(self.collection_name)

        return collections

    def create_collection(self, size: int):

        collections = self.client.get_collections()
        indexed = next((collection for collection in collections.collections if collection.name == self.collection_name), None)
        if not indexed:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=size, distance=Distance.COSINE),
                on_disk_payload=True
            )
        else:
            print(f"Collections {self.collection_name} already exists")

    def delete_collection(self, collection_name: str):

        try:
            self.client.delete_collection(collection_name)
        except Exception as e:
            print(f"Collection cannot be deleted,  error: {e}")

    def upsert_to_collection(self, points: list):

        print('Upserting')

        self.client.upsert(
            collection_name=self.collection_name,
            wait=True,
            points=[
                PointStruct(id=point['id'], vector=point['vector'], payload=point['payload']) for point in points
            ]
        )

    def search(self, query_embedding):

        search_result = self.client.search(
            self.collection_name,
            query_vector=query_embedding,
            limit=1,
            search_params=models.SearchParams(hnsw_ef=128, exact=False),
        )

        return search_result

