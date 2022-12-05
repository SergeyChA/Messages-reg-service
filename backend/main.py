import asyncio
import tornado.web
import tornado.ioloop
import os
import json
from aio_pika import Message, connect_robust


class FormHandler(tornado.web.RequestHandler):
    async def get(self) -> None:
        self.render("main.html", title="Обращение")


class SendFormHandler(tornado.web.RequestHandler):
    async def post(self) -> None:
        data = json.dumps({
            'surname': self.get_argument('surname'),
            'name': self.get_argument('name'),
            'patronymic': self.get_argument('patronymic'),
            'phone': self.get_argument('phone'),
            'message': self.get_argument('message')
        })
        connection = await connect_robust("amqp://guest:guest@rabbitmq/")
        async with connection:
            routing_key = "queue"
            channel = await connection.channel()

            await channel.default_exchange.publish(
                Message(body=data.encode("utf-8")),
                routing_key=routing_key
            )
        self.redirect(url="/")


async def make_app() -> tornado.web.Application:
    return tornado.web.Application(
        [(r"/", FormHandler), (r"/post", SendFormHandler)],
        static_path=os.path.join(
            os.path.dirname(__file__), "./frontend/static"
        ),
        template_path=os.path.join(
            os.path.dirname(__file__), "./frontend/templates"
        ),
    )


async def main() -> None:
    app = await make_app()
    app.listen(8888)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
