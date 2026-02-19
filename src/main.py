from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.responses import HTMLResponse
from database import engine
from users.models import Base
from books.models import Base 
# И обязательно импортируй модели, чтобы Base их увидел!
from users.models import UserModel
from books.models import BookModel

from users.router import router as users_router
from books.router import router as books_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # для разработки. Обращаться могут все
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/", response_class=HTMLResponse)
async def read_index():
    # Теперь путь будет /app/src/index.html — это точно сработает
    index_path = os.path.join(BASE_DIR, "index.html")
    with open(index_path, encoding="utf-8") as f:
        return f.read()

app.include_router(users_router) #подключает все эндпоинты из router к app
app.include_router(books_router)






# @app.get("/")
# async def root():
#     return {"message": "Сервер работает. Используй /docs или /setup_database"}



@app.post('/setup_database')
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {'msg':'ok'}




