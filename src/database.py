from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select
from fastapi import FastAPI, HTTPException, Depends
from typing import Optional, Annotated

import os
from sqlalchemy.ext.asyncio import create_async_engine

# 1. Получаем путь к папке, где лежит этот файл (database.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Соединяем путь с именем файла
DB_PATH = os.path.join(BASE_DIR, "books.db")

# 3. Подставляем в URL (обязательно 3 слэша после sqlite+aiosqlite)
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

engine = create_async_engine(DATABASE_URL)
new_session = async_sessionmaker(engine, expire_on_commit = False) # фабрика сессий

async def get_session():
    async with new_session() as session:
        yield session

 
sessionDep = Annotated[AsyncSession, Depends(get_session)] # чтоб дальше прокидывать. В атрибутах тип данных, и какую ф-ю будем прокидывать