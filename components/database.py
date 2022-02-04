from config import URL, author_name, number_of_processes, task
from models.base import Base
from models.config import Config
from models.parsed import Parser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def _get_session():
    engine = create_engine('postgresql+psycopg2://postgres:postgresql@192.168.10.101/alexey_grab', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    return session


class ConstantsDatabaseRelation:
    url = URL
    author = author_name
    processes_count = number_of_processes
    task_type = task

    def __init__(self, session):
        self.session = session

    def add_config_data(self):
        self.session.query(Config).delete()
        record = Config(
            url=self.url,
            author_name=self.author,
            number_of_processes=self.processes_count,
            task=self.task_type
        )
        self.session.add(record)
        self.session.commit()

    def get_config_data(self):
        data = []
        records = self.session.query(Config).all()
        for record in records:
            data.append(record.__dict__)
        return data


class AddData:
    def __init__(self, session, author_name, post_name, post_date):
        self.session = session
        self.author_name = author_name
        self.post_name = post_name
        self.post_date = post_date

    def add_data(self):
        record = Parser(
            author_name=self.author_name,
            post_name=self.post_name,
            post_date=self.post_date
        )
        self.session.add(record)
        self.session.commit()


class GetDelData:
    def __init__(self, session):
        self.session = session

    def get_data(self):
        table_data = []
        for row in self.session.query(Parser).all():
            row_dict = row.__dict__
            del row_dict['_sa_instance_state']  # В main при поиске новых постов мы два раза обращаемся к данным в \
            # таблице parser, первый раз, когда понимаем что задача стоит найти новые посты(task=2), второй раз, когда\
            # находимся в бесконечном цикле безпрерывного поиска новых постов, второе обращение в таблицу parser
            # необходимо нам чтобы проверить, существуют ли те посты, которые мы нашли сейчас в том списке данных, \
            # которые мы получили в самом начале. Чтобы убедиться и найти совпадения между ними для удобства сравнения \
            # ключ _sa_instance_state и его значение я удаляю.
            table_data.append(row_dict)
        return table_data

    def del_data(self):
        self.session.query(Parser).delete()
        self.session.commit()
