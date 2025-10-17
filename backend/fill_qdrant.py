import pandas as pd
import re

from application.db.qdrant_repo import QdrantRepository
from application.services.ml import embedding_model
from qdrant_client import models

df = pd.read_csv('data_cleaned.csv', sep=';')


# "POINT (44.003277 56.331576)"
def parse_coordinates(coord_str):
    match = re.match(r'POINT\s*\(([\d.]+)\s+([\d.]+)\)', coord_str.strip())
    if match:
        lat = float(match.group(2))
        lon = float(match.group(1))
        return {'lat': lat, 'lon': lon}
    return {'lat': None, 'lon': None}


coords = df['coordinate'].apply(parse_coordinates)
df['latitude'] = [c['lat'] for c in coords]
df['longitude'] = [c['lon'] for c in coords]

texts_for_embedding = []
payloads = []

for _, row in df.iterrows():
    payload = {
        'id': row['id'],
        'title': row['title'],
        'desc': row['description'],
        'location': {'lat': row['latitude'], 'lon': row['longitude']},
    }
    payloads.append(payload)
    texts_for_embedding.append(f'{payload["title"]} {payload["desc"]}')

repo = QdrantRepository()

repo.create_collection()

print('start embedding')
vectors = embedding_model.multi_call(texts_for_embedding)
print('end_embeding')

points_to_upsert = []
for i, (payload, vector) in enumerate(zip(payloads, vectors)):
    point = models.PointStruct(
        id=payload['id'],
        payload=payload,
        vector=vector,
    )
    points_to_upsert.append(point)

print('Загрузка данных в Qdrant...')
repo.client.upsert(collection_name=repo.collection_name, points=points_to_upsert)

print(f'Загрузка завершена! Всего загружено {len(points_to_upsert)} записей в Qdrant')
