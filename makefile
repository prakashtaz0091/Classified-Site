# Makefile

build:
    docker-compose build

up:
    docker-compose up

migrate:
    docker-compose run web python src/manage.py migrate

createsuperuser:
    docker-compose run web python src/manage.py createsuperuser
