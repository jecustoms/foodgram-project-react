# praktikum_new_diplom
![Foodgram workflow](https://github.com/jecustoms/foodgram-project-react/actions/workflows/foodgram_workflow.yaml/badge.svg)

# Проект Foodgram
Foodgram сделан для публикации рецептов. Авторизованные пользователи
могут подписываться на понравившихся авторов, добавлять рецепты в избранное,
в покупки, скачать список покупок ингредиентов для добавленных в покупки
рецептов.

# Установка
1. Склонировать репозиторий
2. Создать файл `.env' и заполнить его:
```
SECRET_KEY= #ключ django проекта
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=  #имя пользователя postgres
POSTGRES_PASSWORD=  #пароль пользователя postgres
DB_HOST=db
DB_PORT=5432
```

3. Для запуска сервера на локальной машине необходимо сделать следующее:
```
Первый запуск
cd backend/
docker-compose up -d
после запуска контейнеров
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input

Для последующих запусков
cd backend/
docker-compose up -d

```
Документацию к проекту можно посмотреть на странице `api/docs`.
Администрирование доступно на странице `/admin`.
Проект будет запущен и доступен по адресу [localhost](http://localhost).