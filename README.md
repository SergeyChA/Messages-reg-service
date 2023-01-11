# Сервис регистрации обращений.

## Инструменты:
* Python
* Asyncio
* Tornado
* RabbitMQ
* FastApi
* Postgres
* Docker

## Старт:

<pre><code>docker compose up -d</code></pre>

### Описание:

Форма отправки сообщения:

`localhost:80`

RabbitWQ management:

`localhost:15672`<br/>

`Username: guest`<br/>
`Password: guest`<br/>

phpAdmin:

`localhost:8080`<br/>

`System: PostgreSQL`<br/>
`Server: db`<br/>
`Username: postgres`<br/>
`Password: password`<br/>

В consumer добавлена задержка в 20 сек, чтобы видеть трафик сообщений. 

