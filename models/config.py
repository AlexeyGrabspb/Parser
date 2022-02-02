from sqlalchemy import Column, Integer, String
from models.base import Base


class Config(Base):
    __tablename__ = 'config'
    __tableargs__ = {
        'comment': 'Таблица конфигурации парсера'
    }

    id = Column(Integer, primary_key=True, nullable=False)
    url = Column(String, nullable=False, comment='url, который будет парситься')
    author_name = Column(String, nullable=False, comment='Имя блогера, чьи блоги неоюходимо спарсить')
    number_of_processes = Column(Integer, nullable=False, default=1, comment='Кол-во процессов')
    task = Column(Integer, comment='1 - парсить новые посты данного автора,\
     2 - спарсить посты автора за весь период')
