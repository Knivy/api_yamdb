### api_yamdb
Сайт, где пользователи смогут оставлять отзывы на произведения искусства.
Выполнен в рамках обучения на курсе "Python разработчик буткемп" Яндекс Практикума.

Июль 2024.

### Технологии

Python, Django, Django Rest Framework, Pytest, Flake8, JWT, redoc

### Команда проекта

Исполнители:

Альбина Гилязова (https://github.com/Knivy), 

Иннокентий Мотрий (https://github.com/Kentiy2717).

Наставники:

Ритис Бараускас, Николай Минякин. 

Ревьюер:

Денис Унтевский.

### Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/Knivy/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

* Если у вас Linux/macOS

    ```
    python3 -m venv env
    source env/bin/activate
    ```

* Если у вас Windows

    ```
    python -m venv env
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Документация

Документация API и примеры запросов доступны по адресу http://127.0.0.1:8000/redoc/ после запуска локального сервера по инструкции выше.

### Пример запроса

Для получения списка категорий не требуется токен. 

При переходе в браузере по адресу http://127.0.0.1:8000/api/v1/categories/

пользователь получит ответ следующего формата:

```
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{
"name": "string",
"slug": "^-$"
}
]
}
```