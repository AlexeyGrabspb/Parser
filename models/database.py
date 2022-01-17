from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql+psycopg2://alexey:12345@localhost/Parser')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
