from sqlalchemy import Column, Integer, String
from models.base import Base


class Parser(Base):
    __tablename__ = 'parser'
    __tableargs__ = {
        'comment': 'Таблица спарсенных данных определенного пользователя'
    }

    id = Column(Integer, primary_key=True, nullable=False)
    author_name = Column(String, comment='Имя блогера', nullable=False)
    post_name = Column(String, comment='Заголовок поста', nullable=False)
    post_date = Column(String, comment='Дата публикации', nullable=False)
