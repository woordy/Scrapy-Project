# connection.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from scrapy.utils.project import get_project_settings
from .models import Base  # Import Base from your models module


def db_connect():
    """
    Connects to the database using settings from the Scrapy settings file and returns an engine instance.
    """
    settings = get_project_settings()
    return create_engine(settings.get("SQLALCHEMY_DATABASE_URI"))


def create_tables(engine): # type: ignore
    """
    Creates all tables in the database. This should be called only once,
    ideally at the start of the project to setup the database schema.
    """
    Base.metadata.create_all(engine)


@contextmanager
def session_scope():
    """
    Provide a transactional scope around a series of operations.
    """
    engine = db_connect()  # Retrieve the engine via the db_connect function
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
