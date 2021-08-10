# praktikum_new_diplom
[![Foodgram-project-react Workflow](https://github.com/jecustoms/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/jecustoms/foodgram-project-react/actions/workflows/main.yml)

# Проект Foodgram
Foodgram сделан для публикации рецептов. Авторизованные пользователи
могут подписываться на понравившихся авторов, добавлять рецепты в избранное,
в покупки, скачать список покупок ингредиентов для добавленных в покупки
рецептов.

# Проект в интернете
Проект запущен и доступен по адресу [временный адрес](http://178.154.211.129). 

Документацию к проекту можно посмотреть на странице `api/docs`. 

Администрирование доступно на странице `/admin`: логин: review_master, пароль: review2021

# Установка
1. Склонировать репозиторий
2. Создать файл `.env' в папке backend и заполнить его:
```
SECRET_KEY= #ключ django проекта
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME=postgres
POSTGRES_USER=  #имя пользователя postgres
POSTGRES_PASSWORD=  #пароль пользователя postgres
DB_HOST=db
DB_PORT=5432
```

3. Для запуска необходимо сделать следующее:
!ВАЖНО! Для работы сервиса необходим заранее установленный Docker и docker-compose

```
>>> Первый запуск из короневой директории:
docker-compose up -d --build

>>> После запуска контейнеров
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate --no-input
docker-compose exec backend python manage.py collectstatic --no-input

>>> Создаем суперпользователя
docker-compose exec backend python manage.py createsuperuser
```
