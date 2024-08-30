# Core Backend

[![Linters Status](https://github.com/AITH-Courses/CoreBackend/actions/workflows/linters.yaml/badge.svg?branch=master)](https://github.com/AITH-Courses/CoreBackend/actions/workflows/linters.yaml)

## Разработка
### Окружение для разработки
```bash
docker-compose -f dev.docker-compose.yaml up -d
```

### Запуск приложения
```bash
poetry run uvicorn src.app:app --port 5000 --reload
```

### Миграции
```bash
poetry run alembic revision --autogenerate -m "Comment"
poetry run alembic upgrade head
```

### Линтеры
```bash
poetry run ruff check src
```

## Тестирование
### Окружение для тестирования
```bash
docker-compose -f test.docker-compose.yaml up -d
```

### Тесты
```bash
poetry run pytest -v unit_tests 
poetry run pytest -v integration_tests

```