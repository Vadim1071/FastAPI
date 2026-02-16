from books.models import Base, BookModel
from books.shema import BookGetSchema, NewBook
from database import sessionDep
from sqlalchemy import select

from fastapi import APIRouter

router = APIRouter(prefix="/books", tags=["Книги"])



@router.get('/', summary='Все книги', tags=['Книги'], response_model=list[BookGetSchema]) # pydentic схема это то, какой будет ответ снаружи
async def get_books(session: sessionDep):   # создает сессию - передает в асин ф.-цию - после выполнения закрывает
    query = select(BookModel)       #   SELECT * FROM book;
    result = await session.execute(query) # выполнить асин запрос
    return result.scalars().all()    # преобразует в ОРМ объект. Только значения из колонок будут
                                    # Возвращается итератор. Поэтому нужно указать что конкретно показать (scalars().all()) 
    



@router.get("/{id}", summary='Конкретная книга', tags=['Книги'])
async def get_book(id: int, session: sessionDep):
    result = await session.execute(select(BookModel).where(BookModel.id == id)) # Как выше, но в одну строку (SELECT * FROM book WHERE id = :id)
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(404)
    return book # Как выше, но в две строки. Добавили переменную



@router.post('/', summary='Добавить книгу', tags=['Книги'], response_model=BookGetSchema) # провалидирует поля по BookGetSchema в ответе. Там возвращается ОРМ объект
async def add_book(new_book: NewBook, session: sessionDep):  # Добавить книгу. Провалидировать по этой модели. Валидируются данные из сваггера (JSON из тела запроса)
    new_book = BookModel(title=new_book.title, author=new_book.author) # Вот такой объект орм создать. Объект который можно засунуть в базу. Элемент таблицы. Данные сюда пришли через Pydantic
                                                                       # new_book → валидные данные из запроса. BookModel(...) → строка в таблице
    session.add(new_book) # Добавить в базу
    await session.commit()
    return new_book                                                  
