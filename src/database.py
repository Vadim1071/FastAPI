from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select
from fastapi import FastAPI, HTTPException, Depends
from typing import Optional, Annotated

engine = create_async_engine('sqlite+aiosqlite:///books.db') # Создали подключение к БД books.db
new_session = async_sessionmaker(engine, expire_on_commit = False) # фабрика сессий

async def get_session():
    async with new_session() as session:
        yield session

 
sessionDep = Annotated[AsyncSession, Depends(get_session)] # чтоб дальше прокидывать. В атрибутах тип данных, и какую ф-ю будем прокидывать