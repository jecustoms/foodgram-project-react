# praktikum_new_diplom
[![Foodgram-project-react Workflow](https://github.com/jecustoms/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/jecustoms/foodgram-project-react/actions/workflows/main.yml)

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

# Проект Foodgram
Foodgram сделан для публикации рецептов. Авторизованные пользователи
могут подписываться на понравившихся авторов, добавлять рецепты в избранное,
в покупки, скачать список покупок ингредиентов для добавленных в покупки
рецептов.

# Проект в интернете
Проект запущен и доступен по [адресу](http://178.154.211.129). 

Документацию к проекту можно посмотреть на странице `api/docs`. 

Администрирование доступно на странице `/admin`. (почта: review@review.xxx, логин: review_master, пароль: praktikum2021)

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
