# 🚗📸 CarsPlateDetector 
## **Данное приложение является демонстрационным вариантом системы СКУД.**

### Описание:
Приложение на Flask для обработки видео с использованием двух моделей YOLOv11n для задач распознавания и трекинга объектов. 
Это приложение предназначено для детектирования автомобильных номеров и их вывод на страницу.

### 🔧 Функционал
1. 🐳 **Микросервисное приложение**, состоящее из двух сервисов. Полное описание можно найти в **Dockerfile** и **docker-compose.yml**
2. 🏞️ **Frontend** построен на HTML с добавлением лайт скрипта на JS.
3. 🚀 **Backend** для приложения является python с Flask. В другом сервисе используются 2 модели YOLO для трекинга номеров и распознавания символов соответственно.
4. 🌐 **FastAPI**: Используется для отправки имени видеофайла, загруженного пользователем.

### Пример использования
![Снимок экрана 2025-01-27 в 18.06.56.png](ExamplePhotos/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-01-27%20%D0%B2%2018.06.56.png)

![Снимок экрана 2025-01-27 в 18.24.51.png](ExamplePhotos/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-01-27%20%D0%B2%2018.24.51.png)


### 📦 Установка
1. Склонируйте репозиторий
```bash
  git clone https://github.com/Gashkoff/CarsPlateDetector.git
  ```  
2. В директоии AutoDetect запустите docker compose 
```bash
  docker compose up -d
```
3. Подключитесь на localhost:8000.

### 📖 API:
1. Обработка видео

URL: /api  
Method: POST  
DESC: Отправляет имя видеофайла для обработки

Параметры:
- video_name: строка

Пример запроса:
```bash
  curl -X 'POST' \
  'http://127.0.0.1:8002/api' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "video_name": "video.mp4"
}'
```

Ответ:
```json
{
  "symbols": "A000AA000 B111BB00",
  "error_message": "None"
}
```

### 🛠️ Стек 
	•	Flask: Для создания веб-приложения. 
	•	FastAPI: Для отправки запросов между сервисами.
	•	YOLOv11n: Для детекции и трекинга объектов.
	•	OpenCV: Для обработки видео и работы с изображениями.
	•	Docker: Для оректрации контейнеров.

# 💾 Важное дополнение
В данном приложение не реализовано:
- Взаимодействие с базами данных.
- Обработки всех возможных ошибок backend и frontend.
- Авторизации и аутентификации пользователей.
- Многопоточная обработка видео и фото.
- Асинхронное взаимодействие с приложением
- Сохранения запрошенных видео и обработанных данных.

В реальных product-приложениях выше перечисленное либо имеет место быть, либо должно быть реализовано в обязательном порядке