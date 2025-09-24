FROM python:3.12-slim

WORKDIR /app

# Копируем только зависимости
COPY requirements.txt ./

# Ставим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код
COPY . .

CMD ["python", "start.py"]

WORKDIR /web
