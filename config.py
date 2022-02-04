from random import choice

'''Парсер имеет два режима работы, поиск постов автора по всему сайту - task = 1, \
и поиск новых постов автора - task = 2'''

URL = 'https://bikepost.ru/index/'
author_name = 'kim'
number_of_processes = 5
task = 1

useragents = open('useragents.txt').read().split('\n')
proxies = open('proxies.txt').read().split('\n')

proxy = {'http': 'http://' + choice(proxies)}
useragent = {'User-Agent': choice(useragents)}
