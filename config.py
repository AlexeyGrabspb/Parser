from random import choice

'''Парсер имеет два режима работы, поиск постов автора по всему сайту - task = 1, \
и поиск новых постов автора - task = 2'''

URL = 'https://bikepost.ru/index/'
author_name = 'kim'
number_of_processes = 5
task = 1

# try:
#     def row2dict(row):
#         d = {}
#         for column in row.__table__.columns:
#             d[column.name] = str(getattr(row, column.name))
#         return d
#     config_row = session.query(Config).first()
#     config_dict = row2dict(config_row)
# except AttributeError:
#     print('Table Config is empty!')
#     config_dict = {}
#     config_dict['url'], config_dict['author_name'] = 'https://bikepost.ru/index/', 'kim'
#     config_dict['number_of_processes'], config_dict['task'] = 10, 1
#     print('Parse with default values:', config_dict)
#
# URL, author = config_dict['url'], config_dict['author_name']
# number_of_processes, task = config_dict['number_of_processes'], config_dict['task']


useragents = open('useragents.txt').read().split('\n')
proxies = open('proxies.txt').read().split('\n')

proxy = {'http': 'http://' + choice(proxies)}
useragent = {'User-Agent': choice(useragents)}
