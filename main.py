import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

import csv

from config import URL, author, useragent, proxy, number_of_processes, task


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
    post_data = {}

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
            print(f'Author: {author}, post data: {post_data} ')
    return post_data


def write_csv(data):
    with open('coinmarketcap.csv', 'a', encoding='UTF-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow((data['author'], data['title'], data['date']))
        print(f"{data['title']} 'parsed'")


def read_csv():
    with open('coinmarketcap.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        return list(reader)


def make_all(url):
    html = get_html(url)
    data = get_data_post(html)
    write_csv(data)


def main():
    html = get_html(URL)
    pages = get_page_links(html)

    if task == 1:
        with Pool(number_of_processes) as p:
            p.map(make_all, pages)
    else:
        while True:
            post_data = get_data_post(html)
            csv_data = read_csv()
            if len(csv_data) == 0:
                write_csv(post_data)
            else:
                for csv_row in csv_data:
                    if post_data['title'] not in csv_row:
                        write_csv(post_data)


if __name__ == '__main__':
    main()
