import requests
from bs4 import BeautifulSoup

from config import useragent, proxy
from components.database import AddData, GetDelData, _get_session, ConstantsDatabaseRelation
from models.parsed import Parser
from multiprocessing import Process, Queue, Pool


def get_html(url):
    r = requests.get(url, headers=useragent, proxies=proxy)
    return r.text


def get_page_links(html):
    all_links = []
    soup = BeautifulSoup(html, 'lxml')
    page_number = int(soup.find('div', class_='pagination').find('ul').find_all('li')[-1].find('a').text)
    for i in range(1, page_number + 1):
        all_links.append(f'{URL}page{i}')
    return all_links


def get_data_post(html):
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


def get_index_data(url):
    html = get_html(url)
    data = get_data_post(html)
    return data


def config_to_table():
    session = _get_session()
    database = ConstantsDatabaseRelation(session)
    database.add_config_data()


def table_to_constants():
    session = _get_session()
    database = ConstantsDatabaseRelation(session)
    data = database.get_config_data()
    first_row = data[0]
    current_URL = first_row['url']
    current_author_name = first_row['author_name']
    current_number_of_processes = first_row['number_of_processes']
    current_task = first_row['task']
    return current_URL, current_author_name, current_number_of_processes, current_task


def get_data_parser():
    session = _get_session()
    database = GetDelData(session)
    data = database.get_data()
    return data


def del_data_parser():
    session = _get_session()
    database = GetDelData(session)
    database.del_data()


def add_data_parser(data):
    session = _get_session()
    for row in data:
        author_name, post_name, post_date = row['author'], row['title'], row['date']
        database = AddData(session, author_name, post_name, post_date)
        database.add_data()
        print('Added new post in table parser')


def creator(data, queue):
    print('creating data putting it on the queue')
    for item in data:
        queue.put(item)


def thread(queue):
    session = _get_session()
    while True:
        data = queue.get
        print(data, 'is data in process_two')
        # database = AddData(session, author_name, post_name, post_date)
        # item = queue.get()
        # database.add_data()


def main():
    html = get_html(URL)
    pages = get_page_links(html)

    if task == 1:
        # with multiprocessing.Pool(number_of_processes) as p:
        #     p.map(make_all, pages)
        pass
    else:   # Парсим нонстопом, если находим пост, которого нету в бд, добавляем
        while True:
            table_data = get_data_parser()  # Проверяем, текущее наполнение таблицы
            if len(table_data) == 0:    # Если пустая, заносим текущий результат парсинга первой страницы
                html = get_html(URL)
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
    """Создать таблицу config и передать значения констант из config, как значения полей этой таблицы"""
    # config_to_table()

    """Получить строки из таблицы parser"""
    # get_data_parser()

    """Очистить таблицу parser"""
    # del_data_parser()

    """Возвращаем обратно значения с бд и принимаем за текущие константы(бесполезно, но ради практики можно)"""
    URL, author_name, number_of_processes, task = table_to_constants()

    main()

    #
    #
    # proc_queue = Queue()
    #
    # for _ in range(number_of_processes):
    #     parse_proc = Process(target=thread, args=(proc_queue,))
    #     parse_proc.start()
