# QRKot
# Благотворительный фонд поддержки котиков
QRkot - это API для сервиса по сбору средств для финансирования благотворительных проектов.
В сервисе реализована возможность регистрации пользователей, добавления благотворительных проектов.
Реализована возможность формирования отчетов в Google Sheets

### Технологии используемые в проекте:
- Python 3.11.3
- SQLAlchemy 1.4.36
- Fastapi 0.78.0
- Alembic 1.7.7
- Uvicorn 0.17.6
- Aiogoogle 4.2.0

### Как запустить проект:
Клонировать репозиторий:
```
git clone https://github.com/russ044/QRkot_spreadsheets.git
```
Создать и активировать виртуальное окружение:
```
python -m venv venv
.\venv\Scripts\activate
```
Установить зависимостей:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
Создать и заполнить .env -> Пример заполнения в .env-example

Выполнить миграции:
```
alembic upgrade head
```
Запустить:
```
uvicorn app.main:app --reload
```
Документация по API:
- [http://localhost:8000/docs](http://localhost:8000/docs)

### Автор проекта:
- Емцов Антон [russ044](https://github.com/russ044)
