from pydantic import BaseModel


class SaveMessage(BaseModel):
    surname: str
    name: str
    patronymic: str
    phone: str
    message: str