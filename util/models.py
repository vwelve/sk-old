import json
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

Base = declarative_base()


class Guild(Base):
    __tablename__ = "guilds"

    id = Column('id', Integer, primary_key=True)
    gid = Column('gid', BigInteger, unique=True)
    prefix = Column('prefix', String(5))


with open('./config.json') as file:
    engine = create_engine(json.load(file)['engine_url'])

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    session = Session()

    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
