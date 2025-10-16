from application.db.qdrant_repo import QdrantRepository

client = QdrantRepository()

client.create_collection()
