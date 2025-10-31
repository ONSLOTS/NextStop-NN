# NextStop-NN

## Запуск проекта

1. Установить зависимости:
```bash
cd backend
uv sync
```

2. Запустить docker compose и загрузить Qdrant collection из корня проекта:
```bash
make setup
```

Или по отдельности:
```bash
make up          # Запустить docker compose
make load-qdrant # Загрузить Qdrant collection
```

3. Запуск fastAPI.
```bash
cd backend/application
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

4. Тест API
http://0.0.0.0:8001/docs
