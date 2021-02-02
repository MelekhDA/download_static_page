# Тестовое задание

## АПИ

### Архивация страниц

#### POST /archive

    Запрос на архивирование static-файл и самой страницы
    по указанному адресу

<details>

##### Запрос

    header:
    {
        "Content-Type": "application/json"
    }

   	body:
    {
        "url": "https://example.com"
    }

##### Ответ

	{
        "id": 1,
        "success": "url is being processed"
    }

</details>

#### GET /archive/id/

    Запрос на получение архива по <id>

<details>

##### Запрос

   	params:
    {
        "id": 123
    }
    или
    /archive/123/

##### Ответ

	файл расширения *.zip

    header:
    {
        "Content-Disposition": "attachment; filename=<download_filename.zip>"
        "Content-Type": "application/zip"
    }

    status: 200

</details>

## Запуск

    Необходимо задать свои переменные окружения в .env

    Установка пакетов в окружение:
    1) python -m pip install -r requirements.txt

    Манипуляции с миграциями:
    1) python manage.py db init
    2) python manage.py db migrate
    3) python manage.py db upgrade

    Запуск *.py-скриптов:
    1) worker.py
    2) app.py

## Пример

Примеры архивирования сайтов:
    1) *ru.semrush.com* в [archive_semrush.zip](./archive/archive_semrush.zip)
    2) *tssr-frontend.rd-science.com* в [archive_tssr.zip](./archive/archive_tssr.zip)
