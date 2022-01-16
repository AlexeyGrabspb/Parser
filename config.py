from random import choice


'''table parser config'''
URL = 'https://bikepost.ru/index/'
author = 'kim'
number_of_processes = 20
task = 2   # 1 - парсим весь сайт, 2 - парсим без остановки первую страницу


useragents = open('useragents.txt').read().split('\n')
proxies = open('proxies.txt').read().split('\n')

proxy = {'http': 'http://' + choice(proxies)}
useragent = {'User-Agent': choice(useragents)}
