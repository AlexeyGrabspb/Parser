# Blog parser 
Parser uses PostgreSQL driver, multiprocessing, proxy and changeable User-Agent header.

#### Установка:
1. Склонируйте репозиторий
2. Создайте и войдите в вирутальное окружение
3. Установите зависимости:
    - `pip install -r requirements.txt`

#### Настройка
Перед запуском необходимо заполнить поля: URL, author_name, number_of_processes, task, где переменная task = 1 - поиск постов автора по всему сайту, task = 2 - поиск только новых постов автора.
