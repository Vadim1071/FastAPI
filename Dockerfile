FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё содержимое проекта в папку /app
COPY . .

# 1. Меняем main:app на src.main:app
# 2. Меняем порт 8000 на 10000 (стандарт для Render)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "10000"]