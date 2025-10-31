# NextStop-NN

## Запуск проекта

1. Установить зависимости:
```bash
cd backend
uv sync
```

2. Запустить docker compose и загрузить Qdrant collection:
```bash
make setup
```

Или по отдельности:
```bash
make up          # Запустить docker compose
make load-qdrant # Загрузить Qdrant collection
```
