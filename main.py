from fastapi import FastAPI, HTTPException, Depends
from typing import Optional, Annotated
from models import NewBook, UserSchema, Base, BookModel, BookGetSchema, UserModel, UserGetSchema
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select


app = FastAPI()

engine = create_async_engine('sqlite+aiosqlite:///books.db') # Создали подключение к БД books.db
new_session = async_sessionmaker(engine, expire_on_commit = False) # фабрика сессий

async def get_session():
    async with new_session() as session:
        yield session

sessionDep = Annotated[AsyncSession, Depends(get_session)] # чтоб дальше прокидывать. В атрибутах тип данных, и какую ф-ю будем прокидывать

@app.get("/")
async def root():
    return {"message": "Сервер работает. Используй /docs или /setup_database"}



@app.get('/books', summary='Все книги', tags=['Книги'], response_model=list[BookGetSchema]) # pydentic схема это то, какой будет ответ снаружи
async def get_books(session: sessionDep):   # создает сессию - передает в асин ф.-цию - после выполнения закрывает
    query = select(BookModel)       #   SELECT * FROM book;
    result = await session.execute(query) # выполнить асин запрос
    return result.scalars().all()    # преобразует в ОРМ объект. Только значения из колонок будут
                                    # Возвращается итератор. Поэтому нужно указать что конкретно показать (scalars().all()) 
    



@app.get("/books/{id}", summary='Конкретная книга', tags=['Книги'])
async def get_book(id: int, session: sessionDep):
    result = await session.execute(select(BookModel).where(BookModel.id == id)) # Как выше, но в одну строку (SELECT * FROM book WHERE id = :id)
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(404)
    return book # Как выше, но в две строки. Добавили переменную



@app.post('/book', summary='Добавить книгу', tags=['Книги'], response_model=BookGetSchema) # провалидирует поля по BookGetSchema в ответе. Там возвращается ОРМ объект
async def add_book(new_book: NewBook, session: sessionDep):  # Добавить книгу. Провалидировать по этой модели. Валидируются данные из сваггера (JSON из тела запроса)
    new_book = BookModel(title=new_book.title, author=new_book.author) # Вот такой объект орм создать. Объект который можно засунуть в базу. Элемент таблицы. Данные сюда пришли через Pydantic
                                                                       # new_book → валидные данные из запроса. BookModel(...) → строка в таблице
    session.add(new_book) # Добавить в базу
    await session.commit()
    return new_book                                                  




@app.post('/user', summary='Добавить пользователя', tags=['Пользователи'], response_model=UserGetSchema)   
async def add_user(new_user: UserSchema, session: sessionDep):
    new_user = UserModel(name=new_user.name, email=new_user.email)

    session.add(new_user)
    await session.commit()
    return new_user



@app.get('/users', summary='Получить пользователей', tags=['Пользователи'], response_model=list[UserGetSchema])
async def get_users(session: sessionDep):
    query = select(UserModel)
    result = await session.execute(query)
    return result.scalars().all()    # Возвращается итератор. Поэтому нужно указать что конкретно показать (scalars().all())


@app.get("/users/{name}", response_model=UserSchema, summary='Конкретный пользователь', tags=['Пользователи'])
async def get_user(name: str, session: sessionDep):
    result = await session.execute(select(UserModel).where(UserModel.name==name)) #sql запрос. Селект из какой таблица по какому столбцу. Вернет строку (кортеж в ней)
    users = result.scalars.all() # преобразует в ОРМ объект. Только значения из колонок будут
    if not users:
        raise HTTPException(404)
    return users #возврат ОРМ объекта



@app.post('/setup_database')
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {'msg':'ok'}




# if __name__ == "main":
    # uvicorn.run("main:app", host="0.0.0.0")