# Python HTTP-сервер сервиса погоды

<div align="center">
  <img src="https://img.shields.io/badge/Python-4169E1?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009485?style=for-the-badge&logo=FastAPI&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Uvicorn-4051B5?style=for-the-badge&logo=uvicorn&logoColor=white" alt="ASGI">
  <img src="https://img.shields.io/badge/API-FF6C37?style=for-the-badge&logo=postman&logoColor=white" alt="API">
</div>

# Для запуска необходимо:
1. Слонировать репозиторий в локальную папку или распкаовать архив проекта
2. Перейти к расположению папки WeatherService в терминале 
3. Запустить скрипт командой python script.py на Windows или python3 script.py на UNIX-системах

## Описание проекта
Проект представляет собой локально разворачиваемый HTTP-сервис, который предоставляет доступ пользователям к сервису погоды.
Архитектура проекта представляет собой трехслойную модель, отвечающую принципам чистой архитектуры. 
При первом запуске автоматически создается база данных SQLite, состоящая из двух таблиц для хранения данных о пользователях, а также о погоде в сохраненных ими городах.

**Ключевые требования:**
- Реализация на Python с использованием БД SQLite для хранения необходимых данных.
- Обеспечение работы с несколькими пользователями.
- Сохранение данных между перезапусками сервера.
- Чистая структура кода и документация.

Проект разработан в рамках тестового задания [infotecs](https://infotecs.ru) для стажера Python-разработчика и предоставляет следующий функционал:

- RESTful endpoints в общепринятом формате.
- Стандартные CRUD операции с базой данных.
- Доступ к моментальному получению данных о погодных показателях по координатам места.
- Хранение погодных показателей в локальной базе данных для отслеживаемых городов.
- Валидация данных.
- Обработка ошибок с корректной генерацией ответов на ошибки.

## Используемые технологии и пакеты

### Основные зависимости 
- [FastAPI](https://fastapi.tiangolo.com/) - асинхронный HTTP-фреймоврк.
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM для работы с базами данными в коде Python.
- [SQLite](https://www.sqlite.org/) - встраиваемая реляционная система управления базами данных.
- [Pydantic](https://docs.pydantic.dev/latest/) - библиотека, предназначенная для валидации и трансформации данных.
- [Uvicorn](https://uvicorn.dev/) - ASGI-сервер для запуска асинхронных Python-веб-приложений.

## Установка и запуск
После запуска скрипта в командной строке, либо в терминале любой IDE, все необходимые пакеты будут установлены автоматически.
Для того чтобы пакеты установились корректно необходимо иметь на устройстве:

* Python 3.12+
* pip 24.1+

## REST API 

Сервер RESTful API работает по адресу `http://127.0.0.1:8080`. Он предоставляют следующие endpoints:

### **`POST /auth/register/user`**: регистрация пользователя в системе
    
  Пример запроса (json):  
```
{
  "login": "string",
  "password": "string"
}
```
  Коды ответов: 
* `201 OK` - успешное добавление записи в БД
* `422 Bad Request` - неверные параметры

### **`POST /auth/login`**: авторизация
    
  Пример запроса (json):
  ```
{
  "login": "string",
  "password": "string"
}
```
  Коды ответов: 
* `201 OK` - успешное добавление записи в БД
* `422 Bad Request` - неверные параметры
  

### **`GET /weather/current/`**: Запрос погодных параметров на данный момент по координатам места  

   Query параметры:
   * `latitude` - широта в градусах (float)
   * `longitude` - долгота в градусах (float)
  
   Коды ответов:
   * `200 OK` - успешный запрос
   * `404 Not Found` - внешний API недоступен
   * `500 Internal Server Error` - серверная ошибка

### **`GET /weather/cities/`**: Запрос списка городов, сохраненных пользователем 

   Коды ответов:
   * `200 OK` - успешный запрос
   * `500 Internal Server Error` - серверная ошибка

### **`POST /weather/cities/`**: авторизация
    
  Пример запроса (json):
  ```
{
  "latitude": -90,
  "longitude": -180,
  "name": "string"
}
```
  Коды ответов: 
* `201 OK` - успешное добавление записи в БД
* `422 Bad Request` - неверные параметры

### **`GET /weather/forecast/`**: Запрос погодных параметров на данный момент по координатам места  

   Query параметры:
   * `city_id` - id города, хранящегося в БД
   * `at_time` - момент времени, в который отслеживаются параметры
   * `fields` - отслеживаемые погодные параметры. Available values : temperature, humidity, wind_speed, precipitation
  
   Коды ответов:
   * `200 OK` - успешный запрос
   * `404 Not Found` - внешний API недоступен
   * `500 Internal Server Error` - серверная ошибка


## Структура проекта 
```
src
├──main.py
├──core/
│  └──config/
│     └──config.py
├──domain/                      
│  ├──user.py                
│  └──weather.py                   
├──errors/ 
│  └──exceptions.py
├──database/ 
│  └──database.py
└──FeatureWeather        
   ├──repository/                  
   │  ├──models.py                
   │  ├──user.py            
   │  └──weather.py                   
   ├──service/                       
   │  ├──security_service.py               
   │  ├──user.py                                    
   │  └──weather.py
   └──transport/               
      ├──router/                        
      │  ├──auth_router.py                  
      │  └──weather_router.py
      ├──schemas/                      
      │  ├──request.py                   
      │  └──response.py 
      ├──dependencies.py
      ├──mappers.py
      ├──user.py
      └──weather.py 
