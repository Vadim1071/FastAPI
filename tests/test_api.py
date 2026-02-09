import pytest
from httpx import AsyncClient, ASGITransport # чтоб дергать приложение напрямую без ювикорн
from main import app

@pytest.mark.asyncio  # указывает что тест - корутина. Для асинхронных тестов
async def test_get_books():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/books") # вызов тестируемой ручки
        assert response.status_code == 200 # проверить какой статус вернула
        data = response.json() # response хранит весь ответ с сервера. Тут тело ответа списком []
        assert isinstance(data, list)

        print(data) # для отладки


@pytest.mark.asyncio
async def test_add_books():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/book", json = {"title": "Test", "author": "Testov"})
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test"

        print(data)