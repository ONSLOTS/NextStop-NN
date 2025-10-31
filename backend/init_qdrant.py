import os
import subprocess
import tarfile

import requests

QDRANT_SNAPSHOT_URL = (
    'https://github.com/user-attachments/files/23277068/qdrant_snapshot.tar.gz'
)
SNAPSHOT_DIR = '/qdrant/snapshots'
COLLECTION_NAME = 'nn_places'


def download_snapshot() -> None:
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    archive_path = os.path.join(SNAPSHOT_DIR, 'qdrant_snapshot.tar.gz')

    if os.path.exists(os.path.join(SNAPSHOT_DIR, COLLECTION_NAME)):
        print('Коллекция уже существует, пропускаем восстановление.')
        return

    print('Скачиваем snapshot...')
    response = requests.get(QDRANT_SNAPSHOT_URL, stream=True)
    with open(archive_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    with tarfile.open(archive_path, 'r:gz') as tar:
        tar.extractall(SNAPSHOT_DIR)

    print('Восстанавливаем коллекцию...')
    subprocess.run(
        [
            'qdrant',
            'snapshot',
            'restore',
            '--path',
            os.path.join(SNAPSHOT_DIR, COLLECTION_NAME),
        ],
        check=True,
    )

    print('Готово! Коллекция восстановлена.')


if __name__ == '__main__':
    download_snapshot()
