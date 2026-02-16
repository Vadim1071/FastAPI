from pydantic import BaseModel, Field, EmailStr, ConfigDict

class ORMBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class NewBook(BaseModel):
    title: str
    author: str

class BookGetSchema(ORMBaseSchema, NewBook):
    id: int