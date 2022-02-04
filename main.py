import multiprocessing

import requests
from bs4 import BeautifulSoup

from config import useragent, proxy
from components.database import AddData, GetDelData, _get_session, ConstantsDatabaseRelation
from multiprocessing import Process, Queue


def get_html(url):  # Получаем результат парсинга index страницы
    r = requests.get(url, headers=useragent, proxies=proxy)
    return r.text


def get_page_links(html):   # Получаем количество страниц блога и создаем урлы
    all_links = []
    soup = BeautifulSoup(html, 'lxml')
    page_number = int(soup.find('div', class_='pagination').find('ul').find_all('li')[-1].find('a').text)
    for i in range(1, page_number + 1):
        all_links.append(f'{URL}page{i}')
    return all_links


def get_data_post(html):    # Парсим
    URL, author_name, number_of_processes, task = table_to_constants()  # Процесс не видит эти константы,\
    # объявленные в if __name__ == __main__, есть догадки почему, но пока так
    print(f'New proxy & User-Agent: {proxy} & {useragent}')
    soup = BeautifulSoup(html, 'lxml')
    posts = soup.find_all('div', class_='topic')
    data = []
    post_data_list = []

    for post in posts:
        class_info = post.find('ul', class_='info')
        post_info = []

        try:
            post_info.append(post.find('a', class_='title-topic').text)
            post_info.append(class_info.find('a').text)
            all_li = class_info.find_all('li')

            if len(all_li) == 6:
                post_info.append(class_info.find_all('li')[2].text)
            else:
                post_info.append(class_info.find_all('li')[1].text)

            data.extend([post_info])
        except AttributeError:
            pass

    for post in data:
        if author_name in post:
            post_data = {'author': post[1], 'title': post[0], 'date': post[2]}
            print(f'Author: {author_name}, post data: {post_data}')
            post_data_list.append(post_data)
    return post_data_list


def config_to_table():  # Записываем константы из модуля config в таблицу config
    session = _get_session()
    database = ConstantsDatabaseRelation(session)
    database.add_config_data()


def table_to_constants():   # Обращаемся к таблице config за константами URL, author_name, numbers_of_processes, task
    session = _get_session()
    database = ConstantsDatabaseRelation(session)
    data = database.get_config_data()
    first_row = data[0]
    current_URL = first_row['url']
    current_author_name = first_row['author_name']
    current_number_of_processes = first_row['number_of_processes']
    current_task = first_row['task']
    return current_URL, current_author_name, current_number_of_processes, current_task


def get_data_parser():  # Возвращаем всё то, что находится в таблицу parser
    session = _get_session()
    database = GetDelData(session)
    data = database.get_data()
    return data


def del_data_parser():  # Удаляем всё то, что находится в таблице parser
    session = _get_session()
    database = GetDelData(session)
    database.del_data()


def add_data_parser(data):  # Добавляем полученные парсингом author_name, post_name, post_date в таблицу parser
    session = _get_session()
    for row in data:
        author_name, post_name, post_date = row['author'], row['title'], row['date']
        database = AddData(session, author_name, post_name, post_date)
        database.add_data()


def creator_task_one(data, queue):  # Создаем очередь(в частности из списка в котором каждый url это следующая \
    # страница блога)
    print('creating data putting it on the queue')
    for item in data:
        queue.put(item)


def thread_task_one(queue):   # Сам процесс. Парсим урл из созданной очереди и записываем в бд
    while not queue.empty():
        each_url = queue.get()
        html = get_html(each_url)
        data = get_data_post(html)
        for row in data:
            author_name, post_name, post_date = row['author'], row['title'], row['date']
            session = _get_session()
            database = AddData(session, author_name, post_name, post_date)
            database.add_data()
            print('The post has been added')


"""Пока не уверен, что в принципе для какой-либо из задач task=2 нужна multiprocessors... Только если в случае когда\
 таблица хорошо заполнена, перевести список, который содержит в себе наполнение таблицы parser в очередь Queue() и\
  вести поиск совпадений post_name с помощью нескольких процессов."""
# def creator_task_two(data, queue):
#
#
# def thread_task_two(queue):


def main():
    html = get_html(URL)
    pages = get_page_links(html)

    if task == 1:
        proc_queue = Queue()
        process_one = Process(target=creator_task_one, args=(pages, proc_queue))  # Создаем процесс создания очереди из\
        # урлов каждой страницы блога
        process_one.start()
        # process_one.join()  # не работает( По идее, запускаем процесс наполнения очереди proc_queue полученными \
        # урлами, пока все урлы не прийдут в proc_queue не парсим

        for _ in range(number_of_processes):
            process_two = Process(target=thread_task_one, args=(proc_queue, ))  # Создаем процесс парсинга каждого урла\
            # из очереди отдельным процессом
            process_two.start()
            print('thread was created')
        print(multiprocessing.cpu_count(), 'cpu count')   # Количество процессов почему-то в два раза больше, чем надо

    else:   # task == 2 - Парсим нонстопом, если находим пост, которого нету в бд, добавляем
        while True:
            table_data = get_data_parser()  # Проверяем, текущее наполнение таблицы
            if len(table_data) == 0:    # Если пустая, заносим текущий результат парсинга первой страницы
                data = get_data_post(html)
                add_data_parser(data)
            else:    # Если непустая, сверяем с тем что мы получим в текущем цикле и тем какие данные были при \
                # запуске скрипта. Если данные в этом цикле новые - записываем.
                while True:
                    current_table_data = get_data_parser()

                    for row in current_table_data:
                        if row not in table_data:
                            add_data_parser(row)


if __name__ == '__main__':
    """Передаем значения констант, которые мы внесли в config, как значения полей этой таблицы"""
    config_to_table()

    """Возвращаем обратно значения с бд и принимаем за текущие константы(бесполезно, но ради практики можно)"""
    URL, author_name, number_of_processes, task = table_to_constants()

    """mp пока, что реализована только на task = 1(когда парсим весь сайт целиком)"""
    main()

    """Получить строки из таблицы parser"""
    # get_data_parser()

    """Очистить таблицу parser"""
    # del_data_parser()