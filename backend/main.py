import asyncio
import tornado.web
import tornado.ioloop
import os
import json
from aio_pika import Message, connect_robust


class FormHandler(tornado.web.RequestHandler):
    def get(self) -> None:
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
        connection = self.application.settings["connection"]
        channel = await connection.channel()

        try:
            await channel.default_exchange.publish(
                Message(body=data.encode("utf-8")), routing_key="queue",
            )
        finally:
            await channel.close()

        self.redirect(url="/")


async def make_app() -> tornado.web.Application:
    connection = await connect_robust("amqp://guest:guest@rabbitmq/")
    channel = await connection.channel()
    await channel.declare_queue("queue", auto_delete=False)
    
    return tornado.web.Application(
        [(r"/", FormHandler), (r"/post", SendFormHandler)],
        connection=connection,
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
