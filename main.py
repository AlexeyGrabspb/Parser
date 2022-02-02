import requests
from bs4 import BeautifulSoup

from config import useragent, proxy  # task, number_of_processes, URL, author
from components.database import Database, _get_session
from models.parsed import Parser
import multiprocessing


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
        if author in post:
            post_data = {'author': post[1], 'title': post[0], 'date': post[2]}
            print(f'Author: {author}, post data: {post_data}')
            post_data_list.append(post_data)
    return post_data_list


def make_all(url):
    html = get_html(url)
    data = get_data_post(html)
    write_row(data)


def write_row(data):
    for row in data:
        new_row = Parser(author_name=row['author'], post_name=row['title'], post_date=row['date'])
        session.add(new_row)
        print(f"{row['title']} 'parsed'")
    session.commit()


def read_table(table):
    table_data = []
    for row in session.query(table):
        table_data.append(row)
        print(row)
    return table_data


def delete_all_rows(table):
    for conf in session.query(table):
        session.delete(conf)
        session.commit()


def main():


    """Создать запись в таблицу Parser"""
    # make_all(URL)

    """Посмотреть записи """
    # read_table(Parser)

    """Удалить"""
    # delete_all_rows(Parser)
    print('1')

    print('2')
    # html = get_html(URL)
    # pages = get_page_links(html)
    #
    # if task == 1:
    #     with Pool(number_of_processes) as p:
    #         p.map(make_all, pages)
    # else:
    #
    #     while True:
    #         table_data = read_table(Parser)
    #
    #         if len(table_data) == 0:
    #             make_all(URL)


def thread(queue):
    session = _get_session()
    database = Database(session)
    item = queue.get()
    database.add_something()


if __name__ == '__main__':
    proc_queue = multiprocessing.Queue()
    proc_count = 4

    for _ in range(proc_count):
        parse_proc = multiprocessing.Process(target=thread, args=(proc_queue,))
        parse_proc.start()

