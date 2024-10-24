# Приложение на FastAPI с Celery, Redis и PostgreSQL
Это проект на FastAPI, который использует Celery для обработки фоновых задач, Redis как брокер, и PostgreSQL для хранения данных.

## Предварительные требования
Убедитесь, что у вас установлены:
- Docker
- Docker Compose
## Настройка
### 1. Создание файла .env
Создайте файл .env в корневой директории проекта и добавьте в него следующие переменные окружения:

```
POSTGRES_USER=<ваш_пользователь_postgres>
POSTGRES_PASSWORD=<ваш_пароль_postgres>
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=<ваша_база_данных>
JWT_SECRET_KEY=<ваш_секретный_ключ_jwt>
JWT_ALGORITHM=<алгоритм_jwt>
REDIS_HOST=redis
REDIS_PORT=6379
API_TOKEN=<ваш_api_token>
```

В директории notify_bot создайте файл .env, который будет содержать токен вашего бота и информацию для подключения к бэкенду.

Пример файла .env:
``` env
API_TOKEN=ваш-токен-бота
BACKEND_IP=fastapi_app  # или IP-адрес вашего бэкенда
BACKEND_PORT=8000     # порт, на котором работает бэкенд
```

- API_TOKEN: Токен вашего Telegram-бота, который можно получить у [BotFather](https://telegram.me/BotFather). 
- BACKEND_IP: IP-адрес сервера бэкенда, с которым бот будет взаимодействовать. 
- BACKEND_PORT: Порт, на котором работает ваш бэкенд.


### 2. Сборка и запуск приложения
Для запуска приложения FastAPI вместе с Celery, Redis и PostgreSQL с использованием Docker Compose выполните команду:
```
docker-compose up --build
```

Это выполнит следующие действия:

- Соберёт приложение на FastAPI.
- Запустит PostgreSQL для управления базой данных.
- Запустит Redis для очереди задач.
- Запустит Celery для обработки фоновых задач.

### 3. Доступ к приложению
После запуска всех сервисов, вы можете получить доступ к приложению FastAPI по следующему адресу:

```
http://localhost:8000
```

### 4. Работа с Celery
Чтобы проверить статус рабочих процессов Celery или увидеть логи выполнения задач, можно подключиться к логам сервиса Celery:

```
docker-compose logs -f celery
```

### 5. Остановка приложения
Для остановки приложения выполните:

```
docker-compose down
```
Это остановит все запущенные контейнеры.

### 6. Очистка
Чтобы удалить все контейнеры, сети и тома, используйте команду:
```
docker-compose down --volumes
```

## Важно

Для того, чтобы пользователь мог связать свой профиль мессенджера и ТГ неоходимо перейти в бота и авторизоваться там.