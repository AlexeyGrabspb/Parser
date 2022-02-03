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


class ConstantsToTable:
    def __init__(self, session, url, author_name, number_of_processes, task):
        self.session = session
        self.url = url
        self.author_name = author_name
        self.number_of_processes = number_of_processes
        self.task = task

    def add_config_data(self):
        self.session.query(Config).delete()
        record = Config(
            url=self.url,
            author_name=self.author_name,
            number_of_processes=self.number_of_processes,
            task=self.task
        )
        self.session.add(record)
        self.session.commit()


class TableToConstants:
    def __init__(self, session):
        self.session = session

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
        # records = self.session.query(Parser).all()
        # for record in records:
        #     print(record.__dict__)

        for row in self.session.query(Parser):
            table_data.append(row)
            print(row)
        return table_data

    def del_data(self):
        self.session.query(Parser).delete()
        self.session.commit()
