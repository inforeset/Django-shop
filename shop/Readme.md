# Django магазин
Это интернет-магазин, написанный на Питоне с использованием фреймворка Django.

## Установка

* Необходимо скопировать все содержимое репозитория в отдельный каталог.

* Установить все библиотеки из `requirements.txt`

* Вводим след. команды в терминале из папки проекта:

```
python manage.py makemigrations
python manage.py migrate
```

* После этого нужно создать суперюзера командой:

```
python manage.py createsuperuser
```
* Нужен установленный сервер RabbitMQ
* Необходимо запустить celery след. командной:
```
celery -A shop.celery_task:app worker -l info -P gevent 
```

* Для мониторинга задач, можно запустить flower, след. командой:
```
celery -A shop.celery_task:app flower
```
После запуска он будет доступен на 5555 порту вашего сайта 

* Теперь можно зайти в админку проекта, по адресу `http://127.0.0.1:8000/admin/`.

* Если необходимо, в проекте присутствуют фикстуры с тестовыми данными, для их загрузки используйте след. команду:

```
python manage.py loaddata fixtures/data.json
```

* В фикстурах суперпользователь: **admin@admin.ru** пароль: **admin** 
* Пароль для остальных пользователей в файле `app_users/pass.txt`