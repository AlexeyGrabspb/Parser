from config import URL, author_name, number_of_processes, task
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
        # records = self.session.query(Parser).all()
        # for record in records:
        #     print(record.__dict__)

        for row in self.session.query(Parser).all():
            row_dict = row.__dict__
            del row_dict['_sa_instance_state']
            table_data.append(row_dict)
        return table_data

    def del_data(self):
        self.session.query(Parser).delete()
        self.session.commit()
