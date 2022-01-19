from sqlalchemy import Column, Integer, String

from models.database import Base


class Parser(Base):
    __tablename__ = 'Parser'
    __tableargs__ = {
        'comment': 'Таблица спарсенных данных определенного пользователя'
    }

    id = Column(Integer, primary_key=True)
    author_name = Column(String(128), comment='Имя блогера')
    post_name = Column(String(128), comment='Заголовок поста')
    post_date = Column(String(128), comment='Дата публикации')

    def __init__(self, author_name: str, post_name: str, post_date: str):
        self.author_name = author_name
        self.post_name = post_name
        self.post_date = post_date

    def __repr__(self):
        return f'{self.author_name} {self.post_name} {self.post_date}'


class Config(Base):
    __tablename__ = 'Config'
    __tableargs__ = {
        'comment': 'Таблица конфигурации парсера'
    }

    id = Column(Integer, primary_key=True)
    url = Column(String, comment='url, который будет парситься')
    author_name = Column(String, comment='Имя блогера, чьи блоги неоюходимо спарсить')
    number_of_processes = Column(Integer, comment='Кол-во процессов')
    task = Column(Integer, comment='1 - парсить новые посты данного автора,\
     2 - спарсить посты автора за весь период')

    def __init__(self, url: str, author_name: str, number_of_processes: str, task: int):
        self.url = url
        self.author_name = author_name
        self.number_of_processes = number_of_processes
        self.task = task

    def __repr__(self):
        return f'{self.url} {self.author_name} {self.number_of_processes} {self.task}'
