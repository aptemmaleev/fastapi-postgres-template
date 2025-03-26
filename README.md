# Миграции

## Шаг 1: Установка Alembic
```
pip install alembic asyncpg
```

## Шаг 2: Инициализация Alembic
```
alembic init migrations
```

## Шаг 3: Применение миграций
```
alembic revision --autogenerate -m "add embedding field"
alembic upgrade head
```


## Ограничения
Значение Enum'ов не обновляется при миграциях. Если требуется их частое обновление, тогда лучше просто использовать Literal. В таком случае валидация типов ложится на плечи pydantic.