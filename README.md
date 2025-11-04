# Hotel Management System - FastAPI

Система управління готелем, реалізована на FastAPI без UI. REST API для управління номерами готелю, бронюваннями та орендою.

## Архітектура

Проєкт реалізовано з використанням **трьохрівневої архітектури (3-tier architecture)**:

### 1. Data Access Layer (DAL)
- **Технологія**: SQLAlchemy ORM + PostgreSQL
- **Розташування**: `app/models/`, `app/database/`
- **Функції**: Робота з базою даних, ORM моделі, міграції

### 2. Business Logic Layer (BLL)
- **Технологія**: Python класи сервісів
- **Розташування**: `app/services/`
- **Функції**: Бізнес-логіка (валідація, обробка даних, правила роботи готелю)
- **Сервіс**: `HotelService` - головний сервіс з бізнес-логікою

### 3. Presentation Layer (API)
- **Технологія**: FastAPI REST API
- **Розташування**: `app/routers/`, `app/main.py`
- **Функції**: HTTP ендпоінти, валідація запитів, документація

## Dependency Injection

Використовується вбудована система **Dependency Injection** FastAPI через `Depends()`:

```python
# Приклад використання DI в роутері
@router.get("/rooms")
def get_all_rooms(db: Session = Depends(get_db)):
    service = HotelService(db)  # Сервіс ін'єктується з БД сесією
    return service.get_all_rooms()
```

**Переваги DI:**
- Слабка зв'язаність компонентів
- Легке тестування (можна підміняти залежності)
- Управління життєвим циклом об'єктів

## Структура проєкту

```
FastAPIApp/
├── app/
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py         # Налаштування БД, SessionLocal, Base
│   ├── models/
│   │   ├── __init__.py
│   │   ├── enums.py            # RoomStatus, RoomCategory
│   │   ├── room.py             # ORM модель Room
│   │   ├── booking.py          # ORM модель Booking
│   │   ├── rental.py           # ORM модель Rental
│   │   └── schemas.py          # Pydantic схеми для валідації
│   ├── services/
│   │   ├── __init__.py
│   │   └── hotel_service.py    # Бізнес-логіка (BLL)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── rooms.py            # API для номерів
│   │   ├── bookings.py         # API для бронювань
│   │   ├── rentals.py          # API для оренди
│   │   └── statistics.py       # API для статистики
│   ├── config.py               # Конфігурація застосування
│   ├── dependencies.py         # Dependency Injection
│   └── main.py                 # Головний файл FastAPI
├── example/                    # Оригінальний проєкт з GUI
├── init_demo_data.py           # Скрипт ініціалізації демо-даних
├── requirements.txt            # Python залежності
├── Dockerfile                  # Docker образ для веб-застосування
├── docker-compose.yml          # Docker Compose (веб + БД)
└── README.md                   # Документація

```

## Функціональність

### Основні можливості

1. **Управління номерами**
   - Створення номерів
   - Перегляд всіх номерів (з фільтрами)
   - Пошук вільних номерів за категорією

2. **Бронювання**
   - Бронювання вільних номерів
   - Скасування бронювань
   - Валідація дат (заборона бронювання в минулому)

3. **Оренда**
   - Здача номерів гостям
   - Завершення оренди з розрахунком вартості

4. **Статистика**
   - Загальна кількість номерів
   - Кількість вільних/заброньованих/зданих номерів
   - Відсоток завантаженості готелю

### Категорії номерів

| Категорія       | Ціна (грн/доба) |
|----------------|----------------|
| Стандарт       | 500            |
| Комфорт        | 800            |
| Люкс           | 1200           |
| Президентський | 2000           |

### Статуси номерів

- **Вільний** - номер доступний для бронювання або здачі
- **Заброньований** - номер заброньовано на майбутній період
- **Зданий** - номер в даний момент здано гостю

## Встановлення та запуск

### Варіант 1: Docker Compose (рекомендовано)

```bash
# Клонуйте репозиторій
git clone <repository-url>
cd FastAPIApp

# Запустіть Docker Compose
docker-compose up --build

# Застосування буде доступне на:
# - API: http://localhost:8000
# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

Docker Compose автоматично:
- Запустить PostgreSQL
- Створить таблиці в БД
- Завантажить демо-дані
- Запустить FastAPI застосування

### Варіант 2: Локальний запуск

```bash
# Встановіть Python 3.11+
python --version

# Встановіть PostgreSQL та створіть БД
createdb hotel_db

# Встановіть залежності
pip install -r requirements.txt

# Налаштуйте змінні оточення
cp .env.example .env
# Відредагуйте .env файл з вашими налаштуваннями БД

# Ініціалізуйте БД з демо-даними
python init_demo_data.py

# Запустіть застосування
uvicorn app.main:app --reload

# Або через Python
python -m uvicorn app.main:app --reload
```

## API Документація

### Swagger UI (інтерактивна документація)

Відкрийте в браузері: `http://localhost:8000/docs`

Тут ви можете:
- Переглянути всі доступні ендпоінти
- Протестувати API прямо в браузері
- Переглянути схеми даних
- Подивитись приклади запитів/відповідей

### ReDoc

Альтернативна документація: `http://localhost:8000/redoc`

### Основні ендпоінти

#### Номери (Rooms)

```bash
# Отримати всі номери
GET /rooms

# Отримати всі номери (з фільтрами)
GET /rooms?category=люкс&status_filter=вільний

# Отримати вільні номери
GET /rooms/free

# Отримати вільні номери певної категорії
GET /rooms/free?category=стандарт

# Отримати конкретний номер
GET /rooms/{room_number}

# Створити номер
POST /rooms
{
  "number": 105,
  "category": "стандарт"
}
```

#### Бронювання (Bookings)

```bash
# Отримати всі бронювання
GET /bookings

# Створити бронювання
POST /bookings
{
  "room_number": 101,
  "guest_name": "Іван Петренко",
  "start_date": "2025-11-10",
  "end_date": "2025-11-15"
}

# Скасувати бронювання
DELETE /bookings/{booking_id}
```

#### Оренда (Rentals)

```bash
# Отримати всі оренди
GET /rentals

# Здати номер
POST /rentals
{
  "room_number": 201,
  "guest_name": "Марія Коваленко",
  "start_date": "2025-11-05",
  "end_date": "2025-11-10"
}

# Завершити оренду
PUT /rentals/{rental_id}/complete
```

#### Статистика (Statistics)

```bash
# Отримати статистику готелю
GET /statistics
```

## Приклади використання

### Приклад 1: Бронювання номеру через curl

```bash
curl -X POST "http://localhost:8000/bookings" \
  -H "Content-Type: application/json" \
  -d '{
    "room_number": 101,
    "guest_name": "Іван Іванов",
    "start_date": "2025-11-10",
    "end_date": "2025-11-15"
  }'
```

### Приклад 2: Пошук вільних номерів

```bash
# Всі вільні номери
curl "http://localhost:8000/rooms/free"

# Вільні номери категорії "люкс"
curl "http://localhost:8000/rooms/free?category=люкс"
```

### Приклад 3: Перегляд статистики

```bash
curl "http://localhost:8000/statistics"
```

## Демо-дані

Скрипт `init_demo_data.py` створює:

- **10 номерів**:
  - 4 стандарт (101-104)
  - 3 комфорт (201-203)
  - 2 люкс (301-302)
  - 1 президентський (401)

- **2 бронювання**:
  - Номер 102: Іван Петренко
  - Номер 301: Олексій Шевченко

- **1 оренда**:
  - Номер 201: Марія Коваленко

## Технології

- **Python 3.11+**
- **FastAPI 0.109.0** - веб-фреймворк
- **SQLAlchemy 2.0** - ORM
- **PostgreSQL 15** - база даних
- **Pydantic 2.5** - валідація даних
- **Uvicorn** - ASGI сервер
- **Docker & Docker Compose** - контейнеризація

## Валідація даних

Застосування автоматично валідує:

- **Дати**: start_date не може бути в минулому
- **Дати**: end_date має бути після start_date
- **Ім'я гостя**: не може бути порожнім
- **Номер кімнати**: має існувати
- **Статус номеру**: можна бронювати/здавати тільки вільні номери

Приклад помилки:

```json
{
  "detail": "Start date cannot be in the past"
}
```

## Зупинка застосування

```bash
# Docker Compose
docker-compose down

# Видалити з даними
docker-compose down -v
```

## Розробка

### Структура коду відповідає принципам:

- **SOLID** принципи
- **Separation of Concerns** (розділення відповідальності)
- **Dependency Injection** для слабкої зв'язаності
- **RESTful API** дизайн

### Розширення функціоналу

Для додавання нового функціоналу:

1. Додайте ORM модель в `app/models/`
2. Додайте Pydantic схеми в `app/models/schemas.py`
3. Розширте `HotelService` в `app/services/hotel_service.py`
4. Створіть роутер в `app/routers/`
5. Підключіть роутер в `app/main.py`

## Тестування

API можна тестувати через:

1. **Swagger UI** (http://localhost:8000/docs) - найпростіший спосіб
2. **curl** - командний рядок
3. **Postman** - GUI клієнт
4. **httpx** - Python бібліотека для тестів

## Ліцензія

MIT

## Автор

Реалізовано як лабораторна робота для демонстрації:
- Трьохрівневої архітектури (DAL → BLL → API)
- Dependency Injection
- REST API без UI
- Docker контейнеризації
