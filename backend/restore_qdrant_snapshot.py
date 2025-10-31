import os
import tarfile
import tempfile
from pathlib import Path

import requests

from application.core.config import settings


def download_snapshot(url: str, output_path: Path) -> None:
    print(f'Скачивание snapshot из {url}...')
    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0

    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    progress = (downloaded / total_size) * 100
                    print(f'\rПрогресс: {progress:.1f}%', end='', flush=True)

    print(f'\nSnapshot успешно скачан в {output_path}')
    print(f'Размер файла: {output_path.stat().st_size / (1024 * 1024):.2f} MB')


def extract_snapshot(tar_path: Path, extract_to: Path) -> Path:
    print(f'\nРаспаковка архива {tar_path.name}...')
    with tarfile.open(tar_path, 'r:gz') as tar:
        tar.extractall(extract_to, filter='data')

    snapshot_files = [
        f for f in extract_to.rglob('*.snapshot')
        if f.is_file() and not f.name.startswith('._')
    ]

    if not snapshot_files:
        all_files = [
            f for f in extract_to.rglob('*')
            if f.is_file() and not f.name.startswith('._')
        ]
        if not all_files:
            raise FileNotFoundError(
                f'Не удалось найти snapshot файл в архиве {tar_path}',
            )
        snapshot_file = max(all_files, key=lambda f: f.stat().st_size)
        print(f'Найден файл: {snapshot_file.name}')
    else:
        snapshot_file = max(snapshot_files, key=lambda f: f.stat().st_size)
        print(f'Найден snapshot файл: {snapshot_file.name}')

    file_size_mb = snapshot_file.stat().st_size / (1024 * 1024)
    print(f'Размер snapshot: {file_size_mb:.2f} MB')

    if snapshot_file.stat().st_size < 1024:
        raise ValueError(
            f'Найденный файл слишком мал ({file_size_mb:.2f} MB), '
            'возможно это файл метаданных, а не snapshot',
        )

    return snapshot_file


def upload_snapshot_to_qdrant(
    snapshot_path: Path,
    collection_name: str,
    qdrant_url: str,
    api_key: str | None = None,
) -> None:
    print('\nЗагрузка snapshot в Qdrant...')
    print(f'URL: {qdrant_url}')
    print(f'Коллекция: {collection_name}')

    upload_url = f'{qdrant_url}/collections/{collection_name}/snapshots/upload?priority=snapshot'

    headers = {}
    if api_key:
        headers['api-key'] = api_key

    with open(snapshot_path, 'rb') as f:
        files = {'snapshot': (snapshot_path.name, f, 'application/octet-stream')}
        response = requests.post(upload_url, files=files, headers=headers, timeout=300)

    if response.status_code != 200:
        print(f'\nОшибка ответа сервера: {response.status_code}')
        print(f'Тело ответа: {response.text}')
        response.raise_for_status()

    print('Snapshot успешно загружен в Qdrant!')


def main() -> None:
    snapshot_url = 'https://github.com/user-attachments/files/23277068/qdrant_snapshot.tar.gz'
    qdrant_url = settings.qdrant.connection_string
    collection_name = settings.qdrant.collection
    api_key = os.getenv('QDRANT_API_KEY')  

    with tempfile.TemporaryDirectory() as temp_dir:
        snapshot_path = Path(temp_dir) / 'qdrant_snapshot.tar.gz'

        try:
            download_snapshot(snapshot_url, snapshot_path)

            extracted_snapshot = extract_snapshot(snapshot_path, Path(temp_dir))

            upload_snapshot_to_qdrant(
                snapshot_path=extracted_snapshot,
                collection_name=collection_name,
                qdrant_url=qdrant_url,
                api_key=api_key,
            )

            print('\n✓ Восстановление завершено успешно!')

        except requests.exceptions.RequestException as e:
            print(f'\n✗ Ошибка при работе с API: {e}')
            raise
        except Exception as e:
            print(f'\n✗ Произошла ошибка: {e}')
            raise


if __name__ == '__main__':
    main()

