# Используем официальный образ Python 3.11 в качестве базового
FROM python:3.11-slim

# Создаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Указываем команду для запуска бота
CMD ["python", "main.py"]