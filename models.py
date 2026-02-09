from pydantic import BaseModel, Field, EmailStr, ConfigDict
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class ORMBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class NewBook(BaseModel):
    title: str
    author: str

class BookGetSchema(ORMBaseSchema, NewBook):
    id: int


class UserSchema(BaseModel):
    email: EmailStr
    name: str


class UserGetSchema(ORMBaseSchema, UserSchema):
    id: int
    
   


class Base(DeclarativeBase):
    pass


class BookModel(Base): #Для ОРМ
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[int]
    author: Mapped[int]


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()