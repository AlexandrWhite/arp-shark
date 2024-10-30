Создать виртуальное окружение
```
python -m venv .venv
```

Установить библиотеки
```
pip install -r requirements.txt
```

Создать файл .env и указать 
```
MYSQL_URL=mysql://<username>:<password>@<host>:<port>/<database_name>
```