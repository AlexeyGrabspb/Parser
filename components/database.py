from models.base import Base
from models.config import Config
from models.parsed import Parser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def _get_session():
    engine = create_engine('postgresql+psycopg2://alexey:12345@localhost/Parser', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    return session


class ConfigTableRelation:
    def __init__(self, session, url, author_name, number_of_processes, task):
        self.session = session
        self.url = url
        self.author_name = author_name
        self.number_of_processes = number_of_processes
        self.task = task

    def add_config_data(self):
        record = Config(
            url=self.url,
            author_name=self.author_name,
            number_of_processes=self.number_of_processes,
            task=self.task
        )
        self.session.add(record)
        self.session.commit()

    def get_config_data(self):
        records = self.session.query(Config).all()
        for record in records:
            print(record.__dict__)


class Database:
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

    def get_data(self):
        records = self.session.query(Parser).all()
        for record in records:
            print(record.__dict__)
