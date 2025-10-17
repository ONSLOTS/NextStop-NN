from qdrant_client import QdrantClient, models

from application.core.config import settings
from application.models.place_payload import PlacePayload


class QdrantRepository:
    def __init__(self) -> None:
        self.client = QdrantClient(url=settings.qdrant.connection_string)
        self.collection_name = settings.qdrant.collection

    def create_collection(self) -> None:
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=settings.qdrant.vector_size,
                    distance=models.Distance.COSINE,
                ),
            )

    def search(self, vector: list[float], top_k: int = 10) -> list[PlacePayload]:
        """
        Searches for the top-k places based on semantic similarity to the user's query.

        Args:
            vector (List[float]): query vector
            top_k (int): number of nearest places to return

        Returns:
            List[PlacePayload]: a list of places with metadata and score
        """
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=top_k,
        )

        output: list[PlacePayload] = []

        for point in results.points:
            raw_payload = point.payload or {}

            payload_data = {
                'id': raw_payload.get('id'),
                'title': raw_payload.get('title'),
                'description': raw_payload.get('desc'),
                'score': point.score,
                'latitude': raw_payload.get('location', {}).get('lat'),
                'longitude': raw_payload.get('location', {}).get('lon'),
            }

            try:
                place = PlacePayload(**payload_data)
                output.append(place)
            except Exception as e:
                print(f'Create PlacePayload error: {e}')

        return output
