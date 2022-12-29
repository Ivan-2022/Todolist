# HOMEWORK_38

Todolist - приложение, планировщик задач.
Проект размещен на домене imeevtodolist.ga

Основной стек: Python3.10, Django, Postgres

Запуск проекта:
- Создать виртуальную среду;
- Установить зависимости - 'pip install -r requirements.txt';
- Установить переменные окружения:
--SECRET_KEY
--POSTGRES_DB
--POSTGRES_USER
--POSTGRES_PASSWORD
--POSTGRES_HOST
--POSTGRES_PORT
--SOCIAL_AUTH_VK_OAUTH2_KEY
--SOCIAL_AUTH_VK_OAUTH2_SECRET
--BOT_API_TOKEN
- Запустить базу данных - 'docker-compose up';
- Выполнить миграции - 'python manage.py makemigrations', 'python manage.py migrate';
- Запустить проект - 'python manage.py runserver'

Цель Homework-38 - Создать бота, который требует подтверждение аккаунта в написанном приложении и через которого можно получать и создавать цели

