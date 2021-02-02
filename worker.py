import os
import pickle
from time import sleep

from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from archive_url import create_zipfile
from settings import STATUS_ARCHIVE_READY

Base = declarative_base()

SLEEP_SECOND = 5
DATABASE = os.getenv('DATABASE')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')


class SitePage(Base):
    """
    Table for archiving pages at specified addresses.
    Used to save created archives.
    """

    __tablename__ = 'site_page'

    id = Column(Integer, primary_key=True)
    url = Column(String())
    zipfile = Column(LargeBinary)
    status = Column(Integer)

    def __init__(self, url: str):
        self.url = url
        self.status = 0

    def __repr__(self) -> str:
        return '<id {}>'.format(self.id)


engine = create_engine(
    f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATABASE}'
)
DBSession = sessionmaker(bind=engine)


def check_request_and_create_zipfile() -> None:
    """
    Generation of archives and saving to the database

    :return: None
    """

    session = DBSession()

    for site_page in session.query(SitePage).filter(SitePage.status != STATUS_ARCHIVE_READY):
        data = create_zipfile(url_page=site_page.url)

        site_page.zipfile = pickle.dumps(data)
        site_page.status = STATUS_ARCHIVE_READY
        session.add(site_page)
        session.commit()

    session.close()


while True:
    check_request_and_create_zipfile()
    sleep(SLEEP_SECOND)
