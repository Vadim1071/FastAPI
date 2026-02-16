from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from users.router import router as users_router
from books.router import router as books_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # для разработки. Обращаться могут все
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", encoding="utf-8") as f:
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




