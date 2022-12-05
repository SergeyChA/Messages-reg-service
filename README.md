# Систему регистрации обращений.

## Инструменты:
* Python
* Tornado
* RabbitMQ
* FastApi
* Postgres
* Docker

## Старт:

docker compose up -d

### Описание:

Форма отправки сообщения:

localhost:80

RabbitWQ management:

localhost:15672
Username: guest
Password: guest

phpAdmin:

localhost:8080
System: PostgreSQL
Server: db
Username: postgres
Password: password

В consumer добавлена задержка в 20 сек, чтобы видеть трафик сообщений. 

